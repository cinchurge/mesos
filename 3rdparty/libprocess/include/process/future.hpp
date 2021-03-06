// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License

#ifndef __PROCESS_FUTURE_HPP__
#define __PROCESS_FUTURE_HPP__

#include <assert.h>

#include <atomic>
#include <list>
#include <memory> // TODO(benh): Replace shared_ptr with unique_ptr.
#include <ostream>
#include <set>
#include <type_traits>
#include <utility>
#include <vector>

#include <glog/logging.h>

#include <process/clock.hpp>
#include <process/latch.hpp>
#include <process/owned.hpp>
#include <process/pid.hpp>
#include <process/timer.hpp>

#include <stout/abort.hpp>
#include <stout/check.hpp>
#include <stout/duration.hpp>
#include <stout/error.hpp>
#include <stout/lambda.hpp>
#include <stout/none.hpp>
#include <stout/option.hpp>
#include <stout/preprocessor.hpp>
#include <stout/result.hpp>
#include <stout/result_of.hpp>
#include <stout/synchronized.hpp>
#include <stout/try.hpp>

#include <stout/os/strerror.hpp>

namespace process {

// Forward declarations (instead of include to break circular dependency).
template <typename G>
struct _Deferred;

template <typename T>
class Future;


namespace internal {

template <typename T>
struct wrap;

template <typename T>
struct unwrap;

} // namespace internal {


// Forward declaration of Promise.
template <typename T>
class Promise;


// Forward declaration of WeakFuture.
template <typename T>
class WeakFuture;

// Forward declaration of Failure.
struct Failure;
struct ErrnoFailure;


// Definition of a "shared" future. A future can hold any
// copy-constructible value. A future is considered "shared" because
// by default a future can be accessed concurrently.
template <typename T>
class Future
{
public:
  // Constructs a failed future.
  static Future<T> failed(const std::string& message);

  Future();

  /*implicit*/ Future(const T& _t);
  /*implicit*/ Future(T&& _t);

  template <typename U>
  /*implicit*/ Future(const U& u);

  /*implicit*/ Future(const Failure& failure);

  /*implicit*/ Future(const ErrnoFailure& failure);

  /*implicit*/ Future(const Future<T>& that) = default;
  /*implicit*/ Future(Future<T>&& that) = default;

  /*implicit*/ Future(const Try<T>& t);

  /*implicit*/ Future(const Try<Future<T>>& t);

  ~Future() = default;

  // Futures are assignable (and copyable). This results in the
  // reference to the previous future data being decremented and a
  // reference to 'that' being incremented.
  Future<T>& operator=(const Future<T>& that) = default;
  Future<T>& operator=(Future<T>&& that) = default;

  // Comparison operators useful for using futures in collections.
  bool operator==(const Future<T>& that) const;
  bool operator!=(const Future<T>& that) const;
  bool operator<(const Future<T>& that) const;

  // Helpers to get the current state of this future.
  bool isPending() const;
  bool isReady() const;
  bool isDiscarded() const;
  bool isFailed() const;
  bool isAbandoned() const;
  bool hasDiscard() const;

  // Discards this future. Returns false if discard has already been
  // called or the future has already completed, i.e., is ready,
  // failed, or discarded. Note that a discard does not terminate any
  // computation but rather acts as a suggestion or indication that
  // the caller no longer cares about the result of some
  // computation. The callee can decide whether or not to continue the
  // computation on their own (where best practices are to attempt to
  // stop the computation if possible). The callee can discard the
  // computation via Promise::discard which completes a future, at
  // which point, Future::isDiscarded is true (and the
  // Future::onDiscarded callbacks are executed). Before that point,
  // but after calling Future::discard, only Future::hasDiscard will
  // return true and the Future::onDiscard callbacks will be invoked.
  bool discard();

  // Waits for this future to become ready, discarded, or failed.
  bool await(const Duration& duration = Seconds(-1)) const;

  // Return the value associated with this future, waits indefinitely
  // until a value gets associated or until the future is discarded.
  const T& get() const;
  const T* operator->() const;

  // Returns the failure message associated with this future.
  const std::string& failure() const;

  // Type of the callback functions that can get invoked when the
  // future gets set, fails, or is discarded.
  typedef lambda::CallableOnce<void()> AbandonedCallback;
  typedef lambda::CallableOnce<void()> DiscardCallback;
  typedef lambda::CallableOnce<void(const T&)> ReadyCallback;
  typedef lambda::CallableOnce<void(const std::string&)> FailedCallback;
  typedef lambda::CallableOnce<void()> DiscardedCallback;
  typedef lambda::CallableOnce<void(const Future<T>&)> AnyCallback;

  // Installs callbacks for the specified events and returns a const
  // reference to 'this' in order to easily support chaining.
  const Future<T>& onAbandoned(AbandonedCallback&& callback) const;
  const Future<T>& onDiscard(DiscardCallback&& callback) const;
  const Future<T>& onReady(ReadyCallback&& callback) const;
  const Future<T>& onFailed(FailedCallback&& callback) const;
  const Future<T>& onDiscarded(DiscardedCallback&& callback) const;
  const Future<T>& onAny(AnyCallback&& callback) const;

  // TODO(benh): Add onReady, onFailed, onAny for _Deferred<F> where F
  // is not expected.

  template <typename F>
  const Future<T>& onAbandoned(_Deferred<F>&& deferred) const
  {
    return onAbandoned(
        std::move(deferred).operator lambda::CallableOnce<void()>());
  }

  template <typename F>
  const Future<T>& onDiscard(_Deferred<F>&& deferred) const
  {
    return onDiscard(
        std::move(deferred).operator lambda::CallableOnce<void()>());
  }

  template <typename F>
  const Future<T>& onReady(_Deferred<F>&& deferred) const
  {
    return onReady(
        std::move(deferred).operator lambda::CallableOnce<void(const T&)>());
  }

  template <typename F>
  const Future<T>& onFailed(_Deferred<F>&& deferred) const
  {
    return onFailed(std::move(deferred)
        .operator lambda::CallableOnce<void(const std::string&)>());
  }

  template <typename F>
  const Future<T>& onDiscarded(_Deferred<F>&& deferred) const
  {
    return onDiscarded(
        std::move(deferred).operator lambda::CallableOnce<void()>());
  }

  template <typename F>
  const Future<T>& onAny(_Deferred<F>&& deferred) const
  {
    return onAny(std::move(deferred)
        .operator lambda::CallableOnce<void(const Future<T>&)>());
  }

private:
  // We use the 'Prefer' and 'LessPrefer' structs as a way to prefer
  // one function over the other when doing SFINAE for the 'onReady',
  // 'onFailed', 'onAny', and 'then' functions. In each of these cases
  // we prefer calling the version of the functor that takes in an
  // argument (i.e., 'const T&' for 'onReady' and 'then' and 'const
  // std::string&' for 'onFailed'), but we allow functors that don't
  // care about the argument. We don't need to do this for
  // 'onDiscard', 'onDiscarded' or 'onAbandoned' because they don't
  // take an argument.
  struct LessPrefer {};
  struct Prefer : LessPrefer {};

  template <typename F, typename = typename result_of<F(const T&)>::type>
  const Future<T>& onReady(F&& f, Prefer) const
  {
    return onReady(lambda::CallableOnce<void(const T&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const T& t) {
              std::move(f)(t);
            },
            std::forward<F>(f),
            lambda::_1)));
  }

  // This is the less preferred `onReady`, we prefer the `onReady` method which
  // has `f` taking a `const T&` parameter. Unfortunately, to complicate
  // matters, if `F` is the result of a `std::bind` expression we need to SFINAE
  // out this version of `onReady` and force the use of the preferred `onReady`
  // (which works because `std::bind` will just ignore the `const T&` argument).
  // This is necessary because Visual Studio 2015 doesn't support using the
  // `std::bind` call operator with `result_of` as it's technically not a
  // requirement by the C++ standard.
  template <
      typename F,
      typename = typename result_of<typename std::enable_if<
          !std::is_bind_expression<typename std::decay<F>::type>::value,
          F>::type()>::type>
  const Future<T>& onReady(F&& f, LessPrefer) const
  {
    return onReady(lambda::CallableOnce<void(const T&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const T&) {
              std::move(f)();
            },
            std::forward<F>(f),
            lambda::_1)));
  }

  template <typename F, typename = typename result_of<F(const std::string&)>::type> // NOLINT(whitespace/line_length)
  const Future<T>& onFailed(F&& f, Prefer) const
  {
    return onFailed(lambda::CallableOnce<void(const std::string&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const std::string& message) {
              std::move(f)(message);
            },
            std::forward<F>(f),
            lambda::_1)));
  }

  // Refer to the less preferred version of `onReady` for why these SFINAE
  // conditions are necessary.
  template <
      typename F,
      typename = typename result_of<typename std::enable_if<
          !std::is_bind_expression<typename std::decay<F>::type>::value,
          F>::type()>::type>
  const Future<T>& onFailed(F&& f, LessPrefer) const
  {
    return onFailed(lambda::CallableOnce<void(const std::string&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const std::string&) mutable {
              std::move(f)();
            },
            std::forward<F>(f),
            lambda::_1)));
  }

  template <typename F, typename = typename result_of<F(const Future<T>&)>::type> // NOLINT(whitespace/line_length)
  const Future<T>& onAny(F&& f, Prefer) const
  {
    return onAny(lambda::CallableOnce<void(const Future<T>&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const Future<T>& future) {
              std::move(f)(future);
            },
            std::forward<F>(f),
            lambda::_1)));
  }

  // Refer to the less preferred version of `onReady` for why these SFINAE
  // conditions are necessary.
  template <
      typename F,
      typename = typename result_of<typename std::enable_if<
          !std::is_bind_expression<typename std::decay<F>::type>::value,
          F>::type()>::type>
  const Future<T>& onAny(F&& f, LessPrefer) const
  {
    return onAny(lambda::CallableOnce<void(const Future<T>&)>(
        lambda::partial(
            [](typename std::decay<F>::type&& f, const Future<T>&) {
              std::move(f)();
            },
            std::forward<F>(f),
            lambda::_1)));
  }

public:
  template <typename F>
  const Future<T>& onAbandoned(F&& f) const
  {
    return onAbandoned(lambda::CallableOnce<void()>(
        lambda::partial(
            [](typename std::decay<F>::type&& f) {
              std::move(f)();
            },
            std::forward<F>(f))));
  }

  template <typename F>
  const Future<T>& onDiscard(F&& f) const
  {
    return onDiscard(lambda::CallableOnce<void()>(
        lambda::partial(
            [](typename std::decay<F>::type&& f) {
              std::move(f)();
            },
            std::forward<F>(f))));
  }

  template <typename F>
  const Future<T>& onReady(F&& f) const
  {
    return onReady(std::forward<F>(f), Prefer());
  }

  template <typename F>
  const Future<T>& onFailed(F&& f) const
  {
    return onFailed(std::forward<F>(f), Prefer());
  }

  template <typename F>
  const Future<T>& onDiscarded(F&& f) const
  {
    return onDiscarded(lambda::CallableOnce<void()>(
        lambda::partial(
            [](typename std::decay<F>::type&& f) {
              std::move(f)();
            },
            std::forward<F>(f))));
  }

  template <typename F>
  const Future<T>& onAny(F&& f) const
  {
    return onAny(std::forward<F>(f), Prefer());
  }

  // Installs callbacks that get executed when this future is ready
  // and associates the result of the callback with the future that is
  // returned to the caller (which may be of a different type).
  template <typename X>
  Future<X> then(lambda::CallableOnce<Future<X>(const T&)> f) const;

  template <typename X>
  Future<X> then(lambda::CallableOnce<X(const T&)> f) const;

  template <typename X>
  Future<X> then(lambda::CallableOnce<Future<X>()> f) const
  {
    return then(lambda::CallableOnce<Future<X>(const T&)>(
        lambda::partial(std::move(f))));
  }

  template <typename X>
  Future<X> then(lambda::CallableOnce<X()> f) const
  {
    return then(lambda::CallableOnce<X(const T&)>(
        lambda::partial(std::move(f))));
  }

private:
  template <
      typename F,
      typename X =
        typename internal::unwrap<typename result_of<F(const T&)>::type>::type>
  Future<X> then(_Deferred<F>&& f, Prefer) const
  {
    // note the then<X> is necessary to not have an infinite loop with
    // then(F&& f)
    return then<X>(
        std::move(f).operator lambda::CallableOnce<Future<X>(const T&)>());
  }

  // Refer to the less preferred version of `onReady` for why these SFINAE
  // conditions are necessary.
  template <
      typename F,
      typename X = typename internal::unwrap<
          typename result_of<typename std::enable_if<
              !std::is_bind_expression<typename std::decay<F>::type>::value,
              F>::type()>::type>::type>
  Future<X> then(_Deferred<F>&& f, LessPrefer) const
  {
    return then<X>(std::move(f).operator lambda::CallableOnce<Future<X>()>());
  }

  template <typename F, typename X = typename internal::unwrap<typename result_of<F(const T&)>::type>::type> // NOLINT(whitespace/line_length)
  Future<X> then(F&& f, Prefer) const
  {
    return then<X>(
        lambda::CallableOnce<Future<X>(const T&)>(std::forward<F>(f)));
  }

  // Refer to the less preferred version of `onReady` for why these SFINAE
  // conditions are necessary.
  template <
      typename F,
      typename X = typename internal::unwrap<
          typename result_of<typename std::enable_if<
              !std::is_bind_expression<typename std::decay<F>::type>::value,
              F>::type()>::type>::type>
  Future<X> then(F&& f, LessPrefer) const
  {
    return then<X>(lambda::CallableOnce<Future<X>()>(std::forward<F>(f)));
  }

public:
  // NOTE: There are two bugs we're dealing with here.
  //   (1) GCC bug where the explicit use of `this->` is required in the
  //       trailing return type: gcc.gnu.org/bugzilla/show_bug.cgi?id=57543
  //   (2) VS 2017 RC bug where the explicit use of `this->` is disallowed.
  //
  // Since VS 2015 and 2017 RC both implement C++14's deduced return type for
  // functions, we simply choose to use that on Windows.
  //
  // TODO(mpark): Remove the trailing return type once we get to C++14.
  template <typename F>
  auto then(F&& f) const
#ifndef __WINDOWS__
    -> decltype(this->then(std::forward<F>(f), Prefer()))
#endif // __WINDOWS__
  {
    return then(std::forward<F>(f), Prefer());
  }

  // Installs callbacks that get executed if this future is abandoned,
  // is discarded, or failed.
  template <typename F>
  Future<T> recover(F&& f) const;

  template <typename F>
  Future<T> recover(_Deferred<F>&& deferred) const
  {
    return recover(
        std::move(deferred)
          .operator lambda::CallableOnce<Future<T>(const Future<T>&)>());
  }

  // TODO(benh): Considering adding a `rescue` function for rescuing
  // abandoned futures.

  // Installs callbacks that get executed if this future completes
  // because it failed.
  Future<T> repair(
      lambda::CallableOnce<Future<T>(const Future<T>&)> f) const;

  // TODO(benh): Add overloads of 'repair' that don't require passing
  // in a function that takes the 'const Future<T>&' parameter and use
  // Prefer/LessPrefer to disambiguate.

  // Invokes the specified function after some duration if this future
  // has not been completed (set, failed, or discarded). Note that
  // this function is agnostic of discard semantics and while it will
  // propagate discarding "up the chain" it will still invoke the
  // specified callback after the specified duration even if 'discard'
  // was called on the returned future.
  Future<T> after(
      const Duration& duration,
      lambda::CallableOnce<Future<T>(const Future<T>&)> f) const;

  // TODO(benh): Add overloads of 'after' that don't require passing
  // in a function that takes the 'const Future<T>&' parameter and use
  // Prefer/LessPrefer to disambiguate.

private:
  template <typename U>
  friend class Future;
  friend class Promise<T>;
  friend class WeakFuture<T>;
  template <typename U>
  friend std::ostream& operator<<(std::ostream&, const Future<U>&);

  enum State
  {
    PENDING,
    READY,
    FAILED,
    DISCARDED,
  };

  struct Data
  {
    Data();
    ~Data() = default;

    void clearAllCallbacks();

    std::atomic_flag lock = ATOMIC_FLAG_INIT;
    State state;
    bool discard;
    bool associated;
    bool abandoned;

    // One of:
    //   1. None, the state is PENDING or DISCARDED.
    //   2. Some, the state is READY.
    //   3. Error, the state is FAILED; 'error()' stores the message.
    Result<T> result;

    std::vector<AbandonedCallback> onAbandonedCallbacks;
    std::vector<DiscardCallback> onDiscardCallbacks;
    std::vector<ReadyCallback> onReadyCallbacks;
    std::vector<FailedCallback> onFailedCallbacks;
    std::vector<DiscardedCallback> onDiscardedCallbacks;
    std::vector<AnyCallback> onAnyCallbacks;
  };

  // Abandons this future. Returns false if the future is already
  // associated or no longer pending. Otherwise returns true and any
  // Future::onAbandoned callbacks wil be run.
  //
  // If `propagating` is true then we'll abandon this future even if
  // it has already been associated. This is important because
  // `~Promise()` will try and abandon and we need to ignore that if
  // the future has been associated since the promise will no longer
  // be setting the future anyway (and is likely the reason it's being
  // destructed, because it's useless). When the future that we've
  // associated with gets abandoned, however, then we need to actually
  // abandon this future too. Here's an example of this:
  //
  // 1:    Owned<Promise<int>> promise1(new Promise<int>());
  // 2:    Owned<Promise<int>> promise2(new Promise<int>());
  // 3:
  // 4:    Future<int> future1 = promise1->future();
  // 5:    Future<int> future2 = promise2->future();
  // 6:
  // 7:    promise1->associate(future2);
  // 8:
  // 9:    promise1.reset();
  // 10:
  // 11:   assert(!future1.isAbandoned());
  // 12:
  // 13:   promise2.reset();
  // 14:
  // 15:   assert(future2.isAbandoned());
  // 16:   assert(future3.isAbandoned());
  //
  // At line 9 `~Promise()` will attempt to abandon the future by
  // calling `abandon()` but since it's been associated we won't do
  // anything. On line 13 the `onAbandoned()` callback will call
  // `abandon(true)` and know we'll actually abandon the future
  // because we're _propagating_ the abandon from the associated
  // future.
  //
  // NOTE: this is an _INTERNAL_ function and should never be exposed
  // or used outside of the implementation.
  bool abandon(bool propagating = false);

  // Sets the value for this future, unless the future is already set,
  // failed, or discarded, in which case it returns false.
  bool set(const T& _t);
  bool set(T&& _t);

  template <typename U>
  bool _set(U&& _u);

  // Sets this future as failed, unless the future is already set,
  // failed, or discarded, in which case it returns false.
  bool fail(const std::string& _message);

  std::shared_ptr<Data> data;
};


namespace internal {

// Helper for executing callbacks that have been registered.
//
// TODO(*): Invoke callbacks in another execution context.
template <typename C, typename... Arguments>
void run(std::vector<C>&& callbacks, Arguments&&... arguments)
{
  for (size_t i = 0; i < callbacks.size(); ++i) {
    std::move(callbacks[i])(std::forward<Arguments>(arguments)...);
  }
}

} // namespace internal {


// Represents a weak reference to a future. This class is used to
// break cyclic dependencies between futures.
template <typename T>
class WeakFuture
{
public:
  explicit WeakFuture(const Future<T>& future);

  // Converts this weak reference to a concrete future. Returns none
  // if the conversion is not successful.
  Option<Future<T>> get() const;

private:
  std::weak_ptr<typename Future<T>::Data> data;
};


template <typename T>
WeakFuture<T>::WeakFuture(const Future<T>& future)
  : data(future.data) {}


template <typename T>
Option<Future<T>> WeakFuture<T>::get() const
{
  Future<T> future;
  future.data = data.lock();

  if (future.data) {
    return future;
  }

  return None();
}


// Helper for creating failed futures.
struct Failure
{
  explicit Failure(const std::string& _message) : message(_message) {}
  explicit Failure(const Error& error) : message(error.message) {}

  const std::string message;
};


struct ErrnoFailure : public Failure
{
  ErrnoFailure() : ErrnoFailure(errno) {}

  explicit ErrnoFailure(int _code)
    : Failure(os::strerror(_code)), code(_code) {}

  explicit ErrnoFailure(const std::string& message)
    : ErrnoFailure(errno, message) {}

  ErrnoFailure(int _code, const std::string& message)
    : Failure(message + ": " + os::strerror(_code)), code(_code) {}

  const int code;
};


// Forward declaration to use as friend below.
namespace internal {
template <typename U>
void discarded(Future<U> future);
} // namespace internal {


// TODO(benh): Make Promise a subclass of Future?
template <typename T>
class Promise
{
public:
  Promise();
  explicit Promise(const T& t);
  virtual ~Promise();

  Promise(Promise<T>&& that);

  bool discard();
  bool set(const T& _t);
  bool set(T&& _t);
  bool set(const Future<T>& future); // Alias for associate.
  bool associate(const Future<T>& future);
  bool fail(const std::string& message);

  // Returns a copy of the future associated with this promise.
  Future<T> future() const;

private:
  template <typename U>
  friend class Future;
  template <typename U>
  friend void internal::discarded(Future<U> future);

  template <typename U>
  bool _set(U&& u);

  // Not copyable, not assignable.
  Promise(const Promise<T>&);
  Promise<T>& operator=(const Promise<T>&);

  // Helper for doing the work of actually discarding a future (called
  // from Promise::discard as well as internal::discarded).
  static bool discard(Future<T> future);

  Future<T> f;
};


template <>
class Promise<void>;


template <typename T>
class Promise<T&>;


namespace internal {

// Discards a weak future. If the weak future is invalid (i.e., the
// future it references to has already been destroyed), this operation
// is treated as a no-op.
template <typename T>
void discard(WeakFuture<T> reference)
{
  Option<Future<T>> future = reference.get();
  if (future.isSome()) {
    Future<T> future_ = future.get();
    future_.discard();
  }
}


// Helper for invoking Promise::discard in an onDiscarded callback
// (since the onDiscarded callback requires returning void we can't
// bind with Promise::discard).
template <typename T>
void discarded(Future<T> future)
{
  Promise<T>::discard(future);
}

} // namespace internal {


template <typename T>
Promise<T>::Promise()
{
  // Need to "unset" `abandoned` since it gets set in the empty
  // constructor for `Future`.
  f.data->abandoned = false;
}


template <typename T>
Promise<T>::Promise(const T& t)
  : f(t) {}


template <typename T>
Promise<T>::~Promise()
{
  // Note that we don't discard the promise as we don't want to give
  // the illusion that any computation hasn't started (or possibly
  // finished) in the event that computation is "visible" by other
  // means. However, we try and abandon the future if it hasn't been
  // associated or set (or moved, i.e., `f.data` is true).
  if (f.data) {
    f.abandon();
  }
}


template <typename T>
Promise<T>::Promise(Promise<T>&& that)
  : f(std::move(that.f)) {}


template <typename T>
bool Promise<T>::discard()
{
  if (!f.data->associated) {
    return discard(f);
  }
  return false;
}


template <typename T>
bool Promise<T>::set(T&& t)
{
  return _set(std::move(t));
}


template <typename T>
bool Promise<T>::set(const T& t)
{
  return _set(t);
}


template <typename T>
template <typename U>
bool Promise<T>::_set(U&& u)
{
  if (!f.data->associated) {
    return f.set(std::forward<U>(u));
  }
  return false;
}


template <typename T>
bool Promise<T>::set(const Future<T>& future)
{
  return associate(future);
}


template <typename T>
bool Promise<T>::associate(const Future<T>& future)
{
  bool associated = false;

  synchronized (f.data->lock) {
    // Don't associate if this promise has completed. Note that this
    // does not include if Future::discard was called on this future
    // since in that case that would still leave the future PENDING
    // (note that we cover that case below).
    if (f.data->state == Future<T>::PENDING && !f.data->associated) {
      associated = f.data->associated = true;

      // After this point we don't allow 'f' to be completed via the
      // promise since we've set 'associated' but Future::discard on
      // 'f' might get called which will get propagated via the
      // 'f.onDiscard' below. Note that we currently don't propagate a
      // discard from 'future.onDiscard' but these semantics might
      // change if/when we make 'f' and 'future' true aliases of one
      // another.
    }
  }

  // Note that we do the actual associating after releasing the lock
  // above to avoid deadlocking by attempting to require the lock
  // within from invoking 'f.onDiscard' and/or 'f.set/fail' via the
  // bind statements from doing 'future.onReady/onFailed'.
  if (associated) {
    // TODO(jieyu): Make 'f' a true alias of 'future'. Currently, only
    // 'discard' is associated in both directions. In other words, if
    // a future gets discarded, the other future will also get
    // discarded.  For 'set' and 'fail', they are associated only in
    // one direction.  In other words, calling 'set' or 'fail' on this
    // promise will not affect the result of the future that we
    // associated.
    f.onDiscard(lambda::bind(&internal::discard<T>, WeakFuture<T>(future)));

    // Need to disambiguate for the compiler.
    bool (Future<T>::*set)(const T&) = &Future<T>::set;

    future
      .onReady(lambda::bind(set, f, lambda::_1))
      .onFailed(lambda::bind(&Future<T>::fail, f, lambda::_1))
      .onDiscarded(lambda::bind(&internal::discarded<T>, f))
      .onAbandoned(lambda::bind(&Future<T>::abandon, f, true));
  }

  return associated;
}


template <typename T>
bool Promise<T>::fail(const std::string& message)
{
  if (!f.data->associated) {
    return f.fail(message);
  }
  return false;
}


template <typename T>
Future<T> Promise<T>::future() const
{
  return f;
}


// Internal helper utilities.
namespace internal {

template <typename T>
struct wrap
{
  typedef Future<T> type;
};


template <typename X>
struct wrap<Future<X>>
{
  typedef Future<X> type;
};


template <typename T>
struct unwrap
{
  typedef T type;
};


template <typename X>
struct unwrap<Future<X>>
{
  typedef X type;
};


template <typename T>
void select(
    const Future<T>& future,
    std::shared_ptr<Promise<Future<T>>> promise)
{
  // We never fail the future associated with our promise.
  assert(!promise->future().isFailed());

  if (promise->future().isPending()) { // No-op if it's discarded.
    if (future.isReady()) { // We only set the promise if a future is ready.
      promise->set(future);
    }
  }
}

} // namespace internal {


// TODO(benh): Move select and discard into 'futures' namespace.

// Returns a future that captures any ready future in a set. Note that
// select DOES NOT capture a future that has failed or been discarded.
template <typename T>
Future<Future<T>> select(const std::set<Future<T>>& futures)
{
  std::shared_ptr<Promise<Future<T>>> promise(new Promise<Future<T>>());

  promise->future().onDiscard(
      lambda::bind(&internal::discarded<Future<T>>, promise->future()));

  foreach (const Future<T>& future, futures) {
    future.onAny([=](const Future<T>& f) {
      internal::select(f, promise);
    });
  }

  return promise->future();
}


template <typename T>
void discard(const std::set<Future<T>>& futures)
{
  foreach (Future<T> future, futures) { // Need a non-const copy to discard.
    future.discard();
  }
}


template <typename T>
void discard(const std::list<Future<T>>& futures)
{
  foreach (Future<T> future, futures) { // Need a non-const copy to discard.
    future.discard();
  }
}


template <typename T>
bool Promise<T>::discard(Future<T> future)
{
  bool result = false;

  synchronized (future.data->lock) {
    if (future.data->state == Future<T>::PENDING) {
      future.data->state = Future<T>::DISCARDED;
      result = true;
    }
  }

  // Invoke all callbacks associated with this future being
  // DISCARDED. We don't need a lock because the state is now in
  // DISCARDED so there should not be any concurrent modifications to
  // the callbacks.
  if (result) {
    // NOTE: we rely on the fact that we have `future` to protect
    // ourselves from one of the callbacks erroneously deleting the
    // future. In `Future::_set()` and `Future::fail()` we have to
    // explicitly take a copy to protect ourselves.
    internal::run(std::move(future.data->onDiscardedCallbacks));
    internal::run(std::move(future.data->onAnyCallbacks), future);

    future.data->clearAllCallbacks();
  }

  return result;
}


template <typename T>
Future<T> Future<T>::failed(const std::string& message)
{
  Future<T> future;
  future.fail(message);
  return future;
}


template <typename T>
Future<T>::Data::Data()
  : state(PENDING),
    discard(false),
    associated(false),
    abandoned(false),
    result(None()) {}


template <typename T>
void Future<T>::Data::clearAllCallbacks()
{
  onAbandonedCallbacks.clear();
  onAnyCallbacks.clear();
  onDiscardCallbacks.clear();
  onDiscardedCallbacks.clear();
  onFailedCallbacks.clear();
  onReadyCallbacks.clear();
}


template <typename T>
Future<T>::Future()
  : data(new Data())
{
  data->abandoned = true;
}


template <typename T>
Future<T>::Future(const T& _t)
  : data(new Data())
{
  set(_t);
}


template <typename T>
Future<T>::Future(T&& _t)
  : data(new Data())
{
  set(std::move(_t));
}


template <typename T>
template <typename U>
Future<T>::Future(const U& u)
  : data(new Data())
{
  set(u);
}


template <typename T>
Future<T>::Future(const Failure& failure)
  : data(new Data())
{
  fail(failure.message);
}


template <typename T>
Future<T>::Future(const ErrnoFailure& failure)
  : data(new Data())
{
  fail(failure.message);
}


template <typename T>
Future<T>::Future(const Try<T>& t)
  : data(new Data())
{
  if (t.isSome()){
    set(t.get());
  } else {
    fail(t.error());
  }
}


template <typename T>
Future<T>::Future(const Try<Future<T>>& t)
  : data(t.isSome() ? t->data : std::shared_ptr<Data>(new Data()))
{
  if (!t.isSome()) {
    fail(t.error());
  }
}


template <typename T>
bool Future<T>::operator==(const Future<T>& that) const
{
  return data == that.data;
}


template <typename T>
bool Future<T>::operator!=(const Future<T>& that) const
{
  return !(*this == that);
}


template <typename T>
bool Future<T>::operator<(const Future<T>& that) const
{
  return data < that.data;
}


template <typename T>
bool Future<T>::discard()
{
  bool result = false;

  std::vector<DiscardCallback> callbacks;
  synchronized (data->lock) {
    if (!data->discard && data->state == PENDING) {
      result = data->discard = true;

      callbacks.swap(data->onDiscardCallbacks);
    }
  }

  // Invoke all callbacks associated with doing a discard on this
  // future. The callbacks get destroyed when we exit from the
  // function.
  if (result) {
    internal::run(std::move(callbacks));
  }

  return result;
}


template <typename T>
bool Future<T>::abandon(bool propagating)
{
  bool result = false;

  std::vector<AbandonedCallback> callbacks;
  synchronized (data->lock) {
    if (!data->abandoned &&
        data->state == PENDING &&
        (!data->associated || propagating)) {
      result = data->abandoned = true;

      callbacks.swap(data->onAbandonedCallbacks);
    }
  }

  // Invoke all callbacks. The callbacks get destroyed when we exit
  // from the function.
  if (result) {
    internal::run(std::move(callbacks));
  }

  return result;
}


template <typename T>
bool Future<T>::isPending() const
{
  return data->state == PENDING;
}


template <typename T>
bool Future<T>::isReady() const
{
  return data->state == READY;
}


template <typename T>
bool Future<T>::isDiscarded() const
{
  return data->state == DISCARDED;
}


template <typename T>
bool Future<T>::isFailed() const
{
  return data->state == FAILED;
}


template <typename T>
bool Future<T>::isAbandoned() const
{
  return data->abandoned;
}


template <typename T>
bool Future<T>::hasDiscard() const
{
  return data->discard;
}


namespace internal {

inline void awaited(Owned<Latch> latch)
{
  latch->trigger();
}

} // namespace internal {


template <typename T>
bool Future<T>::await(const Duration& duration) const
{
  // NOTE: We need to preemptively allocate the Latch on the stack
  // instead of lazily create it in the critical section below because
  // instantiating a Latch requires creating a new process (at the
  // time of writing this comment) which might need to do some
  // synchronization in libprocess which might deadlock if some other
  // code in libprocess is already holding a lock and then attempts to
  // do Promise::set (or something similar) that attempts to acquire
  // the lock that we acquire here. This is an artifact of using
  // Future/Promise within the implementation of libprocess.
  //
  // We mostly only call 'await' in tests so this should not be a
  // performance concern.
  Owned<Latch> latch(new Latch());

  bool pending = false;

  synchronized (data->lock) {
    if (data->state == PENDING) {
      pending = true;
      data->onAnyCallbacks.push_back(lambda::bind(&internal::awaited, latch));
    }
  }

  if (pending) {
    return latch->await(duration);
  }

  return true;
}


template <typename T>
const T& Future<T>::get() const
{
  if (!isReady()) {
    await();
  }

  CHECK(!isPending()) << "Future was in PENDING after await()";
  // We can't use CHECK_READY here due to check.hpp depending on future.hpp.
  if (!isReady()) {
    CHECK(!isFailed()) << "Future::get() but state == FAILED: " << failure();
    CHECK(!isDiscarded()) << "Future::get() but state == DISCARDED";
  }

  assert(data->result.isSome());
  return data->result.get();
}


template <typename T>
const T* Future<T>::operator->() const
{
  return &get();
}


template <typename T>
const std::string& Future<T>::failure() const
{
  if (data->state != FAILED) {
    ABORT("Future::failure() but state != FAILED");
  }

  CHECK_ERROR(data->result);
  return data->result.error();
}


template <typename T>
const Future<T>& Future<T>::onAbandoned(AbandonedCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->abandoned) {
      run = true;
    } else if (data->state == PENDING) {
      data->onAbandonedCallbacks.emplace_back(std::move(callback));
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(); // NOLINT(misc-use-after-move)
  }

  return *this;
}


template <typename T>
const Future<T>& Future<T>::onDiscard(DiscardCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->discard) {
      run = true;
    } else if (data->state == PENDING) {
      data->onDiscardCallbacks.emplace_back(std::move(callback));
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(); // NOLINT(misc-use-after-move)
  }

  return *this;
}


template <typename T>
const Future<T>& Future<T>::onReady(ReadyCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->state == READY) {
      run = true;
    } else if (data->state == PENDING) {
      data->onReadyCallbacks.emplace_back(std::move(callback));
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(data->result.get()); // NOLINT(misc-use-after-move)
  }

  return *this;
}


template <typename T>
const Future<T>& Future<T>::onFailed(FailedCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->state == FAILED) {
      run = true;
    } else if (data->state == PENDING) {
      data->onFailedCallbacks.emplace_back(std::move(callback));
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(data->result.error()); // NOLINT(misc-use-after-move)
  }

  return *this;
}


template <typename T>
const Future<T>& Future<T>::onDiscarded(DiscardedCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->state == DISCARDED) {
      run = true;
    } else if (data->state == PENDING) {
      data->onDiscardedCallbacks.emplace_back(std::move(callback));
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(); // NOLINT(misc-use-after-move)
  }

  return *this;
}


template <typename T>
const Future<T>& Future<T>::onAny(AnyCallback&& callback) const
{
  bool run = false;

  synchronized (data->lock) {
    if (data->state == PENDING) {
      data->onAnyCallbacks.emplace_back(std::move(callback));
    } else {
      run = true;
    }
  }

  // TODO(*): Invoke callback in another execution context.
  if (run) {
    std::move(callback)(*this); // NOLINT(misc-use-after-move)
  }

  return *this;
}

namespace internal {

// NOTE: We need to name this 'thenf' versus 'then' to distinguish it
// from the function 'then' whose parameter 'f' doesn't return a
// Future since the compiler can't properly infer otherwise.
template <typename T, typename X>
void thenf(lambda::CallableOnce<Future<X>(const T&)>&& f,
           std::unique_ptr<Promise<X>> promise,
           const Future<T>& future)
{
  if (future.isReady()) {
    if (future.hasDiscard()) {
      promise->discard();
    } else {
      promise->associate(std::move(f)(future.get()));
    }
  } else if (future.isFailed()) {
    promise->fail(future.failure());
  } else if (future.isDiscarded()) {
    promise->discard();
  }
}


template <typename T, typename X>
void then(lambda::CallableOnce<X(const T&)>&& f,
          std::unique_ptr<Promise<X>> promise,
          const Future<T>& future)
{
  if (future.isReady()) {
    if (future.hasDiscard()) {
      promise->discard();
    } else {
      promise->set(std::move(f)(future.get()));
    }
  } else if (future.isFailed()) {
    promise->fail(future.failure());
  } else if (future.isDiscarded()) {
    promise->discard();
  }
}


template <typename T>
void repair(
    lambda::CallableOnce<Future<T>(const Future<T>&)>&& f,
    std::unique_ptr<Promise<T>> promise,
    const Future<T>& future)
{
  CHECK(!future.isPending());
  if (future.isFailed()) {
    promise->associate(std::move(f)(future));
  } else {
    promise->associate(future);
  }
}


template <typename T>
void expired(
    const std::shared_ptr<lambda::CallableOnce<Future<T>(const Future<T>&)>>& f,
    const std::shared_ptr<Latch>& latch,
    const std::shared_ptr<Promise<T>>& promise,
    const std::shared_ptr<Option<Timer>>& timer,
    const Future<T>& future)
{
  if (latch->trigger()) {
    // If this callback executed first (i.e., we triggered the latch)
    // then we want to clear out the timer so that we don't hold a
    // circular reference to `future` in it's own `onAny`
    // callbacks. See the comment in `Future::after`.
    *timer = None();

    // Note that we don't bother checking if 'future' has been
    // discarded (i.e., 'future.isDiscarded()' returns true) since
    // there is a race between when we make that check and when we
    // would invoke 'f(future)' so the callee 'f' should ALWAYS check
    // if the future has been discarded and rather than hiding a
    // non-deterministic bug we always call 'f' if the timer has
    // expired.
    promise->associate(std::move(*f)(future));
  }
}


template <typename T>
void after(
    const std::shared_ptr<Latch>& latch,
    const std::shared_ptr<Promise<T>>& promise,
    const std::shared_ptr<Option<Timer>>& timer,
    const Future<T>& future)
{
  CHECK(!future.isPending());
  if (latch->trigger()) {
    // If this callback executes first (i.e., we triggered the latch)
    // it must be the case that `timer` is still some and we can try
    // and cancel the timer.
    CHECK_SOME(*timer);
    Clock::cancel(timer->get());

    // We also force the timer to get deallocated so that there isn't
    // a cicular reference of the timer with itself which keeps around
    // a reference to the original future.
    *timer = None();

    promise->associate(future);
  }
}

} // namespace internal {


template <typename T>
template <typename X>
Future<X> Future<T>::then(lambda::CallableOnce<Future<X>(const T&)> f) const
{
  std::unique_ptr<Promise<X>> promise(new Promise<X>());
  Future<X> future = promise->future();

  lambda::CallableOnce<void(const Future<T>&)> thenf = lambda::partial(
      &internal::thenf<T, X>, std::move(f), std::move(promise), lambda::_1);

  onAny(std::move(thenf));

  onAbandoned([=]() mutable {
    future.abandon();
  });

  // Propagate discarding up the chain. To avoid cyclic dependencies,
  // we keep a weak future in the callback.
  future.onDiscard(lambda::bind(&internal::discard<T>, WeakFuture<T>(*this)));

  return future;
}


template <typename T>
template <typename X>
Future<X> Future<T>::then(lambda::CallableOnce<X(const T&)> f) const
{
  std::unique_ptr<Promise<X>> promise(new Promise<X>());
  Future<X> future = promise->future();

  lambda::CallableOnce<void(const Future<T>&)> then = lambda::partial(
      &internal::then<T, X>, std::move(f), std::move(promise), lambda::_1);

  onAny(std::move(then));

  onAbandoned([=]() mutable {
    future.abandon();
  });

  // Propagate discarding up the chain. To avoid cyclic dependencies,
  // we keep a weak future in the callback.
  future.onDiscard(lambda::bind(&internal::discard<T>, WeakFuture<T>(*this)));

  return future;
}


template <typename T>
template <typename F>
Future<T> Future<T>::recover(F&& f) const
{
  std::shared_ptr<Promise<T>> promise(new Promise<T>());

  const Future<T> future = *this;

  typedef decltype(std::move(f)(future)) R;

  std::shared_ptr<lambda::CallableOnce<R(const Future<T>&)>> callable(
      new lambda::CallableOnce<R(const Future<T>&)>(std::move(f)));

  onAny([=]() {
    if (future.isDiscarded() || future.isFailed()) {
      // We reset `discard` so that if a future gets returned from
      // `f(future)` we won't immediately discard it! We still want to
      // let the future get discarded later, however, hence if it gets
      // set again in the future it'll propagate to the returned
      // future.
      synchronized (promise->f.data->lock) {
        promise->f.data->discard = false;
      }

      promise->set(std::move(*callable)(future));
    } else {
      promise->associate(future);
    }
  });

  onAbandoned([=]() {
    // See comment above for why we reset `discard` here.
    synchronized (promise->f.data->lock) {
      promise->f.data->discard = false;
    }
    promise->set(std::move(*callable)(future));
  });

  // Propagate discarding up the chain. To avoid cyclic dependencies,
  // we keep a weak future in the callback.
  promise->future().onDiscard(
      lambda::bind(&internal::discard<T>, WeakFuture<T>(*this)));

  return promise->future();
}


template <typename T>
Future<T> Future<T>::repair(
    lambda::CallableOnce<Future<T>(const Future<T>&)> f) const
{
  std::unique_ptr<Promise<T>> promise(new Promise<T>());
  Future<T> future = promise->future();

  onAny(lambda::partial(
      &internal::repair<T>, std::move(f), std::move(promise), lambda::_1));

  onAbandoned([=]() mutable {
    future.abandon();
  });

  // Propagate discarding up the chain. To avoid cyclic dependencies,
  // we keep a weak future in the callback.
  future.onDiscard(lambda::bind(&internal::discard<T>, WeakFuture<T>(*this)));

  return future;
}


template <typename T>
Future<T> Future<T>::after(
    const Duration& duration,
    lambda::CallableOnce<Future<T>(const Future<T>&)> f) const
{
  // TODO(benh): Using a Latch here but Once might be cleaner.
  // Unfortunately, Once depends on Future so we can't easily use it
  // from here.
  std::shared_ptr<Latch> latch(new Latch());
  std::shared_ptr<Promise<T>> promise(new Promise<T>());

  // We need to control the lifetime of the timer we create below so
  // that we can force the timer to get deallocated after it
  // expires. The reason we want to force the timer to get deallocated
  // after it expires is because the timer's lambda has a copy of
  // `this` (i.e., a Future) and it's stored in the `onAny` callbacks
  // of `this` thus creating a circular reference. By storing a
  // `shared_ptr<Option<Timer>>` we're able to set the option to none
  // after the timer expires which will deallocate our copy of the
  // timer and leave the `Option<Timer>` stored in the lambda of the
  // `onAny` callback as none. Note that this is safe because the
  // `Latch` makes sure that only one of the callbacks will manipulate
  // the `shared_ptr<Option<Timer>>` so there isn't any concurrency
  // issues we have to worry about.
  std::shared_ptr<Option<Timer>> timer(new Option<Timer>());

  typedef lambda::CallableOnce<Future<T>(const Future<T>&)> F;
  std::shared_ptr<F> callable(new F(std::move(f)));

  // Set up a timer to invoke the callback if this future has not
  // completed. Note that we do not pass a weak reference for this
  // future as we don't want the future to get cleaned up and then
  // have the timer expire because then we wouldn't have a valid
  // future that we could pass to `f`! The reference to `this` that is
  // captured in the timer will get removed by setting the
  // `Option<Timer>` to none (see comment above) either if the timer
  // expires or if `this` completes and we cancel the timer (see
  // `internal::expired` and `internal::after` callbacks for where we
  // force the deallocation of our copy of the timer).
  *timer = Clock::timer(
      duration,
      lambda::bind(&internal::expired<T>, callable, latch, promise, timer,
          *this));

  onAny(lambda::bind(&internal::after<T>, latch, promise, timer, lambda::_1));

  onAbandoned([=]() {
    promise->future().abandon();
  });

  // Propagate discarding up the chain. To avoid cyclic dependencies,
  // we keep a weak future in the callback.
  promise->future().onDiscard(
      lambda::bind(&internal::discard<T>, WeakFuture<T>(*this)));

  return promise->future();
}


template <typename T>
bool Future<T>::set(T&& t)
{
  return _set(std::move(t));
}


template <typename T>
bool Future<T>::set(const T& t)
{
  return _set(t);
}


template <typename T>
template <typename U>
bool Future<T>::_set(U&& u)
{
  bool result = false;

  synchronized (data->lock) {
    if (data->state == PENDING) {
      data->result = std::forward<U>(u);
      data->state = READY;
      result = true;
    }
  }

  // Invoke all callbacks associated with this future being READY. We
  // don't need a lock because the state is now in READY so there
  // should not be any concurrent modifications to the callbacks.
  if (result) {
    // Grab a copy of `data` just in case invoking the callbacks
    // erroneously attempts to delete this future.
    std::shared_ptr<typename Future<T>::Data> copy = data;
    internal::run(std::move(copy->onReadyCallbacks), copy->result.get());
    internal::run(std::move(copy->onAnyCallbacks), *this);

    copy->clearAllCallbacks();
  }

  return result;
}


template <typename T>
bool Future<T>::fail(const std::string& _message)
{
  bool result = false;

  synchronized (data->lock) {
    if (data->state == PENDING) {
      data->result = Result<T>(Error(_message));
      data->state = FAILED;
      result = true;
    }
  }

  // Invoke all callbacks associated with this future being FAILED. We
  // don't need a lock because the state is now in FAILED so there
  // should not be any concurrent modifications to the callbacks.
  if (result) {
    // Grab a copy of `data` just in case invoking the callbacks
    // erroneously attempts to delete this future.
    std::shared_ptr<typename Future<T>::Data> copy = data;
    internal::run(std::move(copy->onFailedCallbacks), copy->result.error());
    internal::run(std::move(copy->onAnyCallbacks), *this);

    copy->clearAllCallbacks();
  }

  return result;
}


template <typename T>
std::ostream& operator<<(std::ostream& stream, const Future<T>& future)
{
  const std::string suffix = future.data->discard ? " (with discard)" : "";

  switch (future.data->state) {
    case Future<T>::PENDING:
      if (future.data->abandoned) {
        return stream << "Abandoned" << suffix;
      }
      return stream << "Pending" << suffix;

    case Future<T>::READY:
      // TODO(benh): Stringify `Future<T>::get()` if it can be
      // stringified (will need to be SFINAE'ed appropriately).
      return stream << "Ready" << suffix;

    case Future<T>::FAILED:
      return stream << "Failed" << suffix << ": " << future.failure();

    case Future<T>::DISCARDED:
      return stream << "Discarded" << suffix;
  }

  return stream;
}


// Helper for setting a set of Promises.
template <typename T>
void setPromises(std::set<Promise<T>*>* promises, const T& t)
{
  foreach (Promise<T>* promise, *promises) {
    promise->set(t);
    delete promise;
  }
  promises->clear();
}


// Helper for failing a set of Promises.
template <typename T>
void failPromises(std::set<Promise<T>*>* promises, const std::string& failure)
{
  foreach (Promise<T>* promise, *promises) {
    promise->fail(failure);
    delete promise;
  }
  promises->clear();
}


// Helper for discarding a set of Promises.
template <typename T>
void discardPromises(std::set<Promise<T>*>* promises)
{
  foreach (Promise<T>* promise, *promises) {
    promise->discard();
    delete promise;
  }
  promises->clear();
}


// Helper for discarding an individual promise in the set.
template <typename T>
void discardPromises(std::set<Promise<T>*>* promises, const Future<T>& future)
{
  foreach (Promise<T>* promise, *promises) {
    if (promise->future() == future) {
      promise->discard();
      promises->erase(promise);
      delete promise;
      return;
    }
  }
}


// Returns a future that will not propagate a discard through to the
// future passed in as an argument. This can be very valuable if you
// want to block some future from getting discarded.
//
// Example:
//
//   Promise<int> promise;
//   Future<int> future = undiscardable(promise.future());
//   future.discard();
//   assert(!promise.future().hasDiscard());
//
// Or another example, when chaining futures:
//
//   Future<int> future = undiscardable(
//       foo()
//         .then([]() { ...; })
//         .then([]() { ...; }));
//
// This will guarantee that a discard _will not_ propagate to `foo()`
// or any of the futures returned from the invocations of `.then()`.
template <typename T>
Future<T> undiscardable(const Future<T>& future)
{
  std::unique_ptr<Promise<T>> promise(new Promise<T>());
  Future<T> future_ = promise->future();
  future.onAny(lambda::partial(
      [](std::unique_ptr<Promise<T>> promise, const Future<T>& future) {
        promise->associate(future);
      },
      std::move(promise),
      lambda::_1));
  return future_;
}


// Decorator that for some callable `f` invokes
// `undiscardable(f(args))` for some `args`. This is used by the
// overload of `undiscardable()` that takes callables instead of a
// specialization of `Future`.
//
// TODO(benh): Factor out a generic decorator pattern to be used in
// other circumstances, e.g., to replace `_Deferred`.
template <typename F>
struct UndiscardableDecorator
{
  template <
    typename G,
    typename std::enable_if<
      std::is_constructible<F, G>::value, int>::type = 0>
  UndiscardableDecorator(G&& g) : f(std::forward<G>(g)) {}

  template <typename... Args>
  auto operator()(Args&&... args)
    -> decltype(std::declval<F&>()(std::forward<Args>(args)...))
  {
    using Result =
      typename std::decay<decltype(f(std::forward<Args>(args)...))>::type;

    static_assert(
        is_specialization_of<Result, Future>::value,
        "Expecting Future<T> to be returned from undiscarded(...)");

    return undiscardable(f(std::forward<Args>(args)...));
  }

  F f;
};


// An overload of `undiscardable()` above that takes and returns a
// callable. The returned callable has decorated the provided callable
// `f` such that when the returned callable is invoked it will in turn
// invoke `undiscardable(f(args))` for some `args`. See
// `UndiscardableDecorator` above for more details.
//
// Example:
//
//   Future<int> future = foo()
//     .then(undiscardable([]() { ...; }));
//
// This guarantees that even if `future` is discarded the discard will
// not propagate into the lambda passed into `.then()`.
template <
    typename F,
    typename std::enable_if<
        !is_specialization_of<typename std::decay<F>::type, Future>::value,
        int>::type = 0>
UndiscardableDecorator<typename std::decay<F>::type> undiscardable(F&& f)
{
  return UndiscardableDecorator<
    typename std::decay<F>::type>(std::forward<F>(f));
}

}  // namespace process {

#endif // __PROCESS_FUTURE_HPP__
