### Required and optional fields for the JSON model file

| Field Name                     | Required | Type    | Description                                                                                                                                      |
| ------------------------------ | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| mlir                           | required | string  | URL that provides the MLIR blob                                                                                                                  |
| device                         | optional | string  | The device to run the threshold tests on                                                                                                         |
| compiler_flags                 | optional | array   | Compiler flag options for the iree compilation                                                                                                   |
| xfail                          | optional | array   | If an array is passed in, the compilation tests will fail on the specified chip, ex: `["gfx90a"]`                                                |
| tuner_file                     | optional | dict    | Adds a `iree-codegen-transform-dialect-library` compiler flag for a SKU-specific tuner file (ex: `{"mi308": "{tuner_file_name}"}`)               |

Please feel free to look at any JSON examples under a model directory (ex: sd3, sdxl)
