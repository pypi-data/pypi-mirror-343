import unittest
from unittest import mock

from energoton import Pool, Task


class TestPool(unittest.TestCase):
    def test_task_by_key(self):
        task_id = "there-is-some-id"

        task = Task(10, id_=task_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        self.assertEqual(pool.get(task_id), task)

        task_id2 = "there-is-another-id"
        task = Task(20, id_=task_id2, name="Task 2")
        pool.add(task)

        self.assertEqual(pool.get(task_id2), task)

    def test_get_embedded_task(self):
        task_id = "there-is-some-id"

        task = Task(10, id_=task_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        root_pool = Pool(children=[pool], name="Root Pool")
        found_task = root_pool.get(task.id)
        self.assertEqual(found_task, task)

    def test_task_already_exists(self):
        same_id = "same-id"

        task = Task(10, id_=same_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        task2 = Task(20, id_=same_id, name="Task 2")

        with self.assertRaises(ValueError):
            pool.add(task2)

    def test_parenting(self):
        task_id = "there-is-some-id"

        task = Task(10, id_=task_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        self.assertEqual(task.parent, pool)

        pool.pop(task_id)

        self.assertIsNone(task.parent)

        new_pool = Pool(name="Pool 2")

        pool.add(new_pool)
        self.assertEqual(new_pool.parent, pool)

        pool.pop(new_pool.id)
        self.assertIsNone(new_pool.parent)

    def test_pop_embedded_task(self):
        task = Task(10, id_="1", name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        root_pool = Pool(children=[pool], name="Root Pool")
        found_task = root_pool.pop(task.id)
        self.assertEqual(found_task, task)

        self.assertEqual(len(root_pool), 1)
        self.assertEqual(len(pool), 0)

    def test_pop_from_embedded_task(self):
        task = Task(10, id_="1")
        p1 = Pool(children=[task], id_="lowest")
        p2 = Pool(children=[p1], id_="middle")
        p3 = Pool(children=[p2], id_="high")

        root_pool = Pool(children=[p3], id_="root")
        found_task = p3.pop(task.id)
        self.assertEqual(found_task, task)

        self.assertTrue(task.id not in root_pool.children)
        self.assertTrue(task.id not in p3.children)
        self.assertTrue(task.id not in p2.children)
        self.assertTrue(task.id not in p1.children)

    def test_iter(self):
        tasks = [Task(i, id_=i) for i in range(5)]
        pool = Pool(children=tasks, name="Pool 1")

        for task in pool:
            self.assertIn(task, tasks)

        self.assertEqual(len(pool), len(tasks))

    def test_is_solved(self):
        tasks = [Task(i, id_=i) for i in range(5)]
        pool = Pool(children=tasks, name="Pool 1")

        self.assertFalse(pool.is_solved)

        for task in tasks:
            task.work_done.append(
                {"task": task, "amount": task.cost, "assignee": mock.Mock()}
            )

        self.assertTrue(pool.is_solved)

    def test_done(self):
        task1 = Task(10, name="Task 1")
        task1.work_done.append(
            {"task": task1, "amount": task1.cost, "assignee": mock.Mock()}
        )

        task2 = Task(20, name="Task 2")

        pool = Pool(children=[task1, task2], name="Pool 1")

        self.assertEqual(list(pool.done), [task1])
        self.assertEqual(list(pool.todo), [task2])

    def test_composite(self):
        task1 = Task(10, name="Task 1")
        task2 = Task(20, name="Task 2")

        task2.work_done.append(
            {"task": task2, "amount": task2.cost, "assignee": mock.Mock()}
        )
        pool1 = Pool(children=[task1, task2], name="Pool 1")

        task3 = Task(30, name="Task 3")
        task4 = Task(40, name="Task 4")
        pool2 = Pool(children=[task3, task4], name="Pool 2")

        task5 = Task(50, name="Task 5")
        task6 = Task(60, name="Task 6")
        task6.work_done.append(
            {"task": task6, "amount": task6.cost, "assignee": mock.Mock()}
        )

        root_pool = Pool(
            children=[pool1, pool2, task5, task6], name="Root Pool"
        )

        self.assertFalse(root_pool.is_solved)

        self.assertEqual(list(root_pool.todo), [pool1, pool2, task5])
        self.assertEqual(list(root_pool.done), [task6])

        # make the first pool solved
        task1.work_done.append(
            {"task": task1, "amount": task1.cost, "assignee": mock.Mock()}
        )
        self.assertEqual(list(root_pool.todo), [pool2, task5])

        # make the second pool solved
        task3.work_done.append(
            {"task": task3, "amount": task3.cost, "assignee": mock.Mock()}
        )
        task4.work_done.append(
            {"task": task4, "amount": task4.cost, "assignee": mock.Mock()}
        )
        self.assertEqual(list(root_pool.todo), [task5])

        # make the last task solved
        task5.work_done.append(
            {"task": task5, "amount": task5.cost, "assignee": mock.Mock()}
        )
        self.assertTrue(root_pool.is_solved)

        self.assertEqual(list(root_pool.done), [pool1, pool2, task5, task6])
        self.assertEqual(list(root_pool.todo), [])

    def test_composite_iter(self):
        task1 = Task(10, name="Task 1")
        task2 = Task(20, name="Task 2")

        pool1 = Pool(children=[task1, task2], name="Pool 1")

        task3 = Task(30, name="Task 3")

        root_pool = Pool(children=[pool1, task3], name="Root Pool")
        self.assertEqual(list(root_pool), [pool1, task3])
