"""
A simple test module, to verify that all the imports and envs are
working as expected.

Try it with the `test.sh` scritp in the `test` folder!

"""

from udapi.core.block import Block


class HelloWorld(Block):
    def process_document(self, document):
        print("Hello, World!")
