# What I would have done with more time

- Create tests for models, all tests are done on a controller level, with 30-45 minutes more I would have tested my models. Although I have created these tests and done full manual testing of all routes, these models have most of the business logic and should be tested to full coverage.
- Create more granular error handling - most functions in my models will return False on error which is a blanket clause for errors, leading to potentially misleading HTTP status codes. Creating my own exceptions to do this and then raising them is also more pythonic and functional.
- Writing more comments. Complete python code would have full docstrings and would pass a pylint scan.
