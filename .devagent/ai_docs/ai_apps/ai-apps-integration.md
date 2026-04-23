---
id: ai-apps-integration
title: Adding AI Apps support to PyrogAI Project
description: Tutorial on adding support for outputs and visualizations to your Project
---

# Adding support for AI Apps

This section will go over how you can prepare your Pyrogai Project for AI Apps integration.

!!! Note "This section is required if you want to use the Standard Template"

If you are using the Dash template, we recommend you follow these steps. However, if you have another preferred method of connecting to your pipeline, you are free to develop with that method.

!!! warning "Disclaimer: If you choose to go down your own development path, you will have very limited AI Apps developer support."

Make sure you have an AI Apps enabled bundle. If you have a bundle that does not have AI Apps enabled,  please read [how to request AI Apps connection](../../provisioning/how-tos/request_aiapps_connection.md)

## Configure outputs from Pyrogai

This section will go over how to set up output results and visualizations. Typically, your outputs should be written to `json` or `csv` file formats in order to be recognized by the application.

#### Specify pipeline outputs

In your `pipeline_<name>.yaml` file under the `src/<project_name>/config/` directory, you will need to specify the outputs from your pipeline. You will need to add a section with the following structure:

```yaml
outputs:
  <output_name_1>:
    type: <output_type>
    path: <output_path>
  <output_name_2>:
    type: <output_type>
    path: <output_path>
  ...
  <output_name_n>:
    type: <output_type>
    path: <output_path>
```

#### Writing outputs

Now, you have successfully created output files for visualization for your application. Make sure you have added this to every file where you specify outputs in your project's pipeline yaml file.

Once you have set this up, you can now begin customization of your application.

### Adding Parameters

If you want to pass in specific parameters when you use your application, you will need to configure these in your `pipeline_<name>.yaml` file under the `src/<project_name>/config/` directory. At the bottom of this file, you will want to add a section with the following structure:

```yaml
params:
    param_1: <param_1 value>
    param_1: <param_1 value>
    ...
    param_n: <param_n value>
```

You will replace `param_1` ... `param_n` with your own custom names and values. To learn more about how these are used, check out the [Form Components](../standard/form-components.md) page.
