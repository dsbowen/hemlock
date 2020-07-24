# Page logic

Now that you've seen compile, validate, submit, and navigate functions, it's time to discuss the logic of hemlock pages.

It's not important to fully understand this now, as long as you have a rough sense of the order in which things happen.

1. **Compile.** The page executes its compile functions. By default, a page's first compile function runs its questions' compile functions.
2. **Render.** The page html is rendered and displayed to the participant.
3. **Record responses.** When the participant submits a page, we record their responses to every question on the page. This sets the questions' `response` attribute.
4. **Validate.** After recording all responses, the page executes its validate functions. By default, a page's first validate function runs its questions' validate functions. When a page or question executes its validate functions, it does so one by one, and if any of them uncover an error (i.e. return a string instead of `None`), validation for that object stops. For example, suppose we attach two validate functions with `Input(validate=[V.require(), V.response_type(float)])`. When the input question runs its validate functions, the first validate function checks that the participant entered a response. Only if they entered a response does the second validate function check that the participant's response can by converted to `float`.
5. **Record data.** The page records the data associated with the participant's responses to every question on the page. This sets the questions' `data` attribute.
6. **Submit.** The page executes its submit functions. By default, a page's first submit function runs its questions' submit functions.
7. **Navigate.** If the page has a navigate function, execute the function and bring the participant to the start of the new branch the function returns. If the page has no navigate function, and the participant has reached the end a a branch, the branch executes its navigate function and brings the participant to the start of the new branch returned by the function.

You can visualize compile functions (validate and submit functions are similar) as follows:

```
Page 1 compile function 1
    Question 1 compile function 1
    Question 1 compile function 2
    ...
    Question 2 compile function 1
    Question 2 compile function 2
    ...
Page 1 compile function 2
...
```

In the next part of the tutorial, we'll give our participants instructions on how to play the ultimatum game and verify their understanding with a comprehension check.