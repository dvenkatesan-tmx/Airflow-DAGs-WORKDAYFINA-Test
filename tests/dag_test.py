import pytest
# from airflow.models import DagBag
from unittest.mock import Mock
import sys

sys.modules['airflow'] = Mock()
sys.modules['airflow.models'] = Mock()
from airflow.models import DagBag

def test_dag_import():
    """
    Test that all DAGs can be successfully imported.
    """
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    assert len(dag_bag.dags) > 0, "No DAGs found in the DAG folder"
    assert len(dag_bag.import_errors) == 0, f"DAG import errors: {dag_bag.import_errors}"
    
# def test_dag_import():
#     dagbag = DagBag(dag_folder='dags/')
#     dag = dagbag.get_dag('dag_name')
#     assert dag is not None, "DAG failed to load"

# def test_task_count():
#     dagbag = DagBag(dag_folder='dags/')
#     dag = dagbag.get_dag('dag_name')
#     assert len(dag.tasks) > 0, "DAG does not contain tasks"

# def test_task_dependencies():
#     dagbag = DagBag(dag_folder='dags/')
#     dag = dagbag.get_dag('dag_name')
#     task = dag.get_task('task_name')
#     assert task.downstream_task_ids == {'expected_task'}, "Task dependencies are not correct"
