import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import math

from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
from azureml.core import Experiment
from azureml.opendatasets import Diabetes
from azureml.core import Run




#Logon to Azure

cli_auth = AzureCliAuthentication()

ws = Workspace(subscription_id="affeac10-5929-43aa-9abd-4ada85acb943",
               resource_group="mlexp",
               workspace_name="ml_workspace",
               auth=cli_auth)

# Create the workspace using the specified parameters
# ws = Workspace.create(name = "ml_workspace", 
#                      subscription_id = "affeac10-5929-43aa-9abd-4ada85acb943", 
#                      resource_group = 'mlexp', 
#                      location = "eastus2", 
#                      create_resource_group = False, 
#                      sku = 'basic', 
#                      exist_ok = True)

# ws.get_details()
# write the details of the workspace to a configuration file to the notebook library
# ws.write_config()

print("Found workspace {} at location {}".format(ws.name, ws.location))

experiment = Experiment(workspace=ws, name="diabetes-experiment")
x_df = Diabetes.get_tabular_dataset().to_pandas_dataframe().dropna()
y_df = x_df.pop("Y")

X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.2, random_state=66)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(X_train)


alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

for alpha in alphas:
    run = experiment.start_logging()
    run.log("alpha_value", alpha)

    model = Ridge(alpha=alpha)
    model.fit(X=X_train, y=y_train)
    y_pred = model.predict(X=X_test)
    rmse = math.sqrt(mean_squared_error(y_true=y_test, y_pred=y_pred))
    run.log("rmse", rmse)

    model_name = "model_alpha_" + str(alpha) + ".pkl"
    filename = "outputs/" + model_name

    joblib.dump(value=model, filename=filename)
    run.upload_file(name=model_name, path_or_stream=filename)
    run.complete()

minimum_rmse_runid = None
minimum_rmse = None

for run in experiment.get_runs():
    run_metrics = run.get_metrics()
    run_details = run.get_details()
    # each logged metric becomes a key in this returned dict
    run_rmse = run_metrics["rmse"]
    run_id = run_details["runId"]

    if minimum_rmse is None:
        minimum_rmse = run_rmse
        minimum_rmse_runid = run_id
    else:
        if run_rmse < minimum_rmse:
            minimum_rmse = run_rmse
            minimum_rmse_runid = run_id

print("Best run_id: " + minimum_rmse_runid)
print("Best run_id rmse: " + str(minimum_rmse))


best_run = Run(experiment=experiment, run_id=minimum_rmse_runid)
print(best_run.get_file_names())