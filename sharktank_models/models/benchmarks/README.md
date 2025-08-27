### Required and optional fields for the JSON model file

| Field Name                     | Required | Type    | Description                                                                                                                                      |
| ------------------------------ | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| inputs                         | optional | array   | An array of objects that provides the input blob and the expected input value (ex: `{"source" :"", "value": ""}`, the value field is optional)   |
| weights                        | optional | array   | (ex: `{"source": "", scope: ""}`), if not provided, will use flat weights.
| modules                        | required | array   | An array containing names of compiled modules to run. The modules should be added in order of dependency.
| device                         | required | string  | The device to run the threshold tests on                                                                                                         |
| compiler_flags                 | optional | array   | Compiler flag options for the iree compilation                                                                                                   |
| run_function                   | optional | string  | The function that the `iree_run_module` in the threshold tests                                                                                   |
| xfail                          | optional | array   | If an array is passed in, the compilation tests will fail on the specified chip, ex: `["gfx90a"]`                                                |

Please feel free to look at any JSON examples under a model directory (ex: sd3, sdxl)
