# Coverage

The aim is to ensure that our tests covers all the lines in our codebase.

However, a line executing during a test does nto mean the test meaningfully exericised the logic. It could pass without checking any real behaviour.

`uv add --dev pytest-cov`
