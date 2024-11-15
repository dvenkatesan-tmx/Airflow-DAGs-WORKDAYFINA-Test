import pytest
from airflow.models import DagBag

def test_dag_import():
    dagbag = DagBag(dag_folder='dags/')
    dag = dagbag.get_dag('dag_name')
    assert dag is not None, "DAG failed to load"

def test_task_count():
    dagbag = DagBag(dag_folder='dags/')
    dag = dagbag.get_dag('dag_name')
    assert len(dag.tasks) > 0, "DAG does not contain tasks"

def test_task_dependencies():
    dagbag = DagBag(dag_folder='dags/')
    dag = dagbag.get_dag('dag_name')
    task = dag.get_task('task_name')
    assert task.downstream_task_ids == {'expected_task'}, "Task dependencies are not correct"
