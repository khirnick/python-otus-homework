"""Testing tools for byterun."""

from __future__ import print_function

import dis
from io import StringIO
import sys
import textwrap
import types
import unittest

from interpreter.byterun import VirtualMachine, VirtualMachineError


# Make this false if you need to run the debugger inside a test.
CAPTURE_STDOUT = ('-s' not in sys.argv)
# Make this false to see the traceback from a failure inside pyvm2.
CAPTURE_EXCEPTION = 1


def dis_code(code):
    """Disassemble `code` and all the code it refers to."""
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            dis_code(const)

    print("")
    print(code)
    dis.dis(code)


class VmTestCase(unittest.TestCase):

    def assert_ok(self, code, raises=None):
        """Run `code` in our VM and in real Python: they behave the same."""

        code = textwrap.dedent(code)
        code = compile(code, "<%s>" % self.id(), "exec", 0, 1)

        # Print the disassembly so we'll see it if the test fails.
        dis_code(code)

        real_stdout = sys.stdout

        # Run the code through our VM.

        vm_stdout = StringIO()
        if CAPTURE_STDOUT:              # pragma: no branch
            sys.stdout = vm_stdout
        vm = VirtualMachine()

        vm_value = vm_exc = None
        try:
            vm_value = vm.run_code(code)
        except VirtualMachineError:         # pragma: no cover
            # If the VM code raises an error, show it.
            raise
        except AssertionError:              # pragma: no cover
            # If test code fails an assert, show it.
            raise
        except Exception as e:
            # Otherwise, keep the exception for comparison later.
            if not CAPTURE_EXCEPTION:       # pragma: no cover
                raise
            vm_exc = e
        finally:
            real_stdout.write("-- stdout ----------\n")
            real_stdout.write(vm_stdout.getvalue())

        # Run the code through the real Python interpreter, for comparison.

        py_stdout = StringIO()
        sys.stdout = py_stdout

        py_value = py_exc = None
        globs = {}
        try:
            py_value = eval(code, globs, globs)
        except AssertionError:              # pragma: no cover
            raise
        except Exception as e:
            py_exc = e

        sys.stdout = real_stdout

        self.assert_same_exception(vm_exc, py_exc)
        self.assertEqual(vm_stdout.getvalue(), py_stdout.getvalue())
        self.assertEqual(vm_value, py_value)
        if raises:
            self.assertIsInstance(vm_exc, raises)
        else:
            self.assertIsNone(vm_exc)

    def assert_same_exception(self, e1, e2):
        """Exceptions don't implement __eq__, check it ourselves."""
        self.assertEqual(str(e1), str(e2))
        self.assertIs(type(e1), type(e2))


class TestFunctions(VmTestCase):
    def test_functions(self):
        self.assert_ok("""\
            def fn(a, b=17, c="Hello", d=[]):
                d.append(99)
                print(a, b, c, d)
            fn(1)
            fn(2, 3)
            fn(3, c="Bye")
            fn(4, d=["What?"])
            fn(5, "b", "c")
            """)

    def test_recursion(self):
        self.assert_ok("""\
            def fact(n):
                if n <= 1:
                    return 1
                else:
                    return n * fact(n-1)
            f6 = fact(6)
            print(f6)
            assert f6 == 720
            """)

    def test_nested_names(self):
        self.assert_ok("""\
            def one():
                x = 1
                def two():
                    x = 2
                    print(x)
                two()
                print(x)
            one()
            """)

    def test_calling_functions_with_args_kwargs(self):
        self.assert_ok("""\
            def fn(a, b=17, c="Hello", d=[]):
                d.append(99)
                print(a, b, c, d)
            fn(6, *[77, 88])
            fn(**{'c': 23, 'a': 7})
            fn(6, *[77], **{'c': 23, 'd': [123]})
            """)

    def test_defining_functions_with_args_kwargs(self):
        self.assert_ok("""\
            def fn(*args):
                print("args is %r" % (args,))
            fn(1, 2)
            """)
        self.assert_ok("""\
            def fn(**kwargs):
                print("kwargs is %r" % (kwargs,))
            fn(red=True, blue=False)
            """)
        self.assert_ok("""\
            def fn(*args, **kwargs):
                print("args is %r" % (args,))
                print("kwargs is %r" % (kwargs,))
            fn(1, 2, red=True, blue=False)
            """)
        self.assert_ok("""\
            def fn(x, y, *args, **kwargs):
                print("x is %r, y is %r" % (x, y))
                print("args is %r" % (args,))
                print("kwargs is %r" % (kwargs,))
            fn('a', 'b', 1, 2, red=True, blue=False)
            """)

    def test_defining_functions_with_empty_args_kwargs(self):
        self.assert_ok("""\
            def fn(*args):
                print("args is %r" % (args,))
            fn()
            """)
        self.assert_ok("""\
            def fn(**kwargs):
                print("kwargs is %r" % (kwargs,))
            fn()
            """)
        self.assert_ok("""\
            def fn(*args, **kwargs):
                print("args is %r, kwargs is %r" % (args, kwargs))
            fn()
            """)

    def test_partial(self):
        self.assert_ok("""\
            from _functools import partial

            def f(a,b):
                return a-b

            f7 = partial(f, 7)
            four = f7(3)
            assert four == 4
            """)

    def test_partial_with_kwargs(self):
        self.assert_ok("""\
            from _functools import partial

            def f(a,b,c=0,d=0):
                return (a,b,c,d)

            f7 = partial(f, b=7, c=1)
            them = f7(10)
            assert them == (10,7,1,0)
            """)

    def test_wraps(self):
        self.assert_ok("""\
            from functools import wraps
            def my_decorator(f):
                dec = wraps(f)
                def wrapper(*args, **kwds):
                    print('Calling decorated function')
                    return f(*args, **kwds)
                wrapper = dec(wrapper)
                return wrapper

            @my_decorator
            def example():
                '''Docstring'''
                return 17

            assert example() == 17
            """)

    def test_different_globals_may_have_different_builtins(self):
        self.assert_ok("""\
            def replace_globals(f, new_globals):
                import sys
                if sys.version_info.major == 2:
                    args = [
                        f.func_code,
                        new_globals,
                        f.func_name,
                        f.func_defaults,
                        f.func_closure,
                    ]
                else:
                    args = [
                        f.__code__,
                        new_globals,
                        f.__name__,
                        f.__defaults__,
                        f.__closure__,
                    ]
                if hasattr(f, '_vm'):
                    name = args.remove(args[2])
                    args.insert(0, name)
                    args.append(f._vm)
                return type(lambda: None)(*args)


            def f():
                assert g() == 2
                assert a == 1


            def g():
                return a  # a is in the builtins and set to 2


            # g and f have different builtins that both provide ``a``.
            g = replace_globals(g, {'__builtins__': {'a': 2}})
            f = replace_globals(f, {'__builtins__': {'a': 1}, 'g': g})


            f()
            """)

    def test_no_builtins(self):
        self.assert_ok("""\
            def replace_globals(f, new_globals):
                import sys


                if sys.version_info.major == 2:
                    args = [
                        f.func_code,
                        new_globals,
                        f.func_name,
                        f.func_defaults,
                        f.func_closure,
                    ]
                else:
                    args = [
                        f.__code__,
                        new_globals,
                        f.__name__,
                        f.__defaults__,
                        f.__closure__,
                    ]
                if hasattr(f, '_vm'):
                    name = args.remove(args[2])
                    args.insert(0, name)
                    args.append(f._vm)
                return type(lambda: None)(*args)


            def f(NameError=NameError, AssertionError=AssertionError):
                # capture NameError and AssertionError early because
                #  we are deleting the builtins
                None
                try:
                    sum
                except NameError:
                    pass
                else:
                    raise AssertionError('sum in the builtins')


            f = replace_globals(f, {})  # no builtins provided
            f()
            """)


class TestClosures(VmTestCase):
    def test_closures(self):
        self.assert_ok("""\
            def make_adder(x):
                def add(y):
                    return x+y
                return add
            a = make_adder(10)
            print(a(7))
            assert a(7) == 17
            """)

    def test_closures_store_deref(self):
        self.assert_ok("""\
            def make_adder(x):
                z = x+1
                def add(y):
                    return x+y+z
                return add
            a = make_adder(10)
            print(a(7))
            assert a(7) == 28
            """)

    def test_closures_in_loop(self):
        self.assert_ok("""\
            def make_fns(x):
                fns = []
                for i in range(x):
                    fns.append(lambda i=i: i)
                return fns
            fns = make_fns(3)
            for f in fns:
                print(f())
            assert (fns[0](), fns[1](), fns[2]()) == (0, 1, 2)
            """)

    def test_closures_with_defaults(self):
        self.assert_ok("""\
            def make_adder(x, y=13, z=43):
                def add(q, r=11):
                    return x+y+z+q+r
                return add
            a = make_adder(10, 17)
            print(a(7))
            assert a(7) == 88
            """)

    def test_deep_closures(self):
        self.assert_ok("""\
            def f1(a):
                b = 2*a
                def f2(c):
                    d = 2*c
                    def f3(e):
                        f = 2*e
                        def f4(g):
                            h = 2*g
                            return a+b+c+d+e+f+g+h
                        return f4
                    return f3
                return f2
            answer = f1(3)(4)(5)(6)
            print(answer)
            assert answer == 54
            """)


class TestGenerators(VmTestCase):
    def test_first(self):
        self.assert_ok("""\
            def two():
                yield 1
                yield 2
            for i in two():
                print(i)
            """)

    def test_partial_generator(self):
        self.assert_ok("""\
            from _functools import partial

            def f(a,b):
                num = a+b
                while num:
                    yield num
                    num -= 1

            f2 = partial(f, 2)
            three = f2(1)
            assert list(three) == [3,2,1]
            """)

    def test_yield_multiple_values(self):
        self.assert_ok("""\
            def triples():
                yield 1, 2, 3
                yield 4, 5, 6

            for a, b, c in triples():
                print(a, b, c)
            """)

    def test_simple_generator(self):
        self.assert_ok("""\
            g = (x for x in [0,1,2])
            print(list(g))
            """)

    def test_generator_from_generator(self):
        self.assert_ok("""\
            g = (x*x for x in range(5))
            h = (y+1 for y in g)
            print(list(h))
            """)

    def test_generator_from_generator2(self):
        self.assert_ok("""\
            class Thing(object):
                RESOURCES = ('abc', 'def')
                def get_abc(self):
                    return "ABC"
                def get_def(self):
                    return "DEF"
                def resource_info(self):
                    for name in self.RESOURCES:
                        get_name = 'get_' + name
                        yield name, getattr(self, get_name)

                def boom(self):
                    #d = list((name, get()) for name, get in self.resource_info())
                    d = [(name, get()) for name, get in self.resource_info()]
                    return d

            print(Thing().boom())
            """)

    def test_yield_from(self):
        self.assert_ok("""\
            def main():
                x = outer()
                next(x)
                y = x.send("Hello, World")
                print(y)

            def outer():
                yield from inner()

            def inner():
                y = yield
                yield y

            main()
            """)

    def test_yield_from_tuple(self):
        self.assert_ok("""\
            def main():
                for x in outer():
                    print(x)

            def outer():
                yield from (1, 2, 3, 4)

            main()
            """)

    def test_distinguish_iterators_and_generators(self):
        self.assert_ok("""\
            class Foo(object):
                def __iter__(self):
                    return FooIter()

            class FooIter(object):
                def __init__(self):
                    self.state = 0

                def __next__(self):
                    if self.state >= 10:
                        raise StopIteration
                    self.state += 1
                    return self.state

                def send(self, n):
                    print("sending")

            def outer():
                yield from Foo()

            for x in outer():
                print(x)
            """)

    def test_nested_yield_from(self):
        self.assert_ok("""\
            def main():
                x = outer()
                next(x)
                y = x.send("Hello, World")
                print(y)

            def outer():
                yield from middle()

            def middle():
                yield from inner()

            def inner():
                y = yield
                yield y

            main()
            """)

    def test_return_from_generator(self):
        self.assert_ok("""\
            def gen():
                yield 1
                return 2

            x = gen()
            while True:
                try:
                    print(next(x))
                except StopIteration as e:
                    print(e.value)
                    break
        """)

    def test_return_from_generator_with_yield_from(self):
        self.assert_ok("""\
            def returner():
                if False:
                    yield
                return 1

            def main():
                y = yield from returner()
                print(y)

            list(main())
        """)