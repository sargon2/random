
import unittest2

# I started writing this because I wanted to figure out the most efficient way to get everything done in the morning before work.
# It turned out to be harder than I expected so I gave up.  The tests are still failing.

class TaskSolver(object):
    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def addTasks(self, *args):
        for task in args:
            self.addTask(task)

    def resolve(self):
        pass

class Task(object):
    def __init__(self, duration):
        self.start = 0
        self.end = self.duration = duration
        self.dependencies = []
        self.conflicts = []

    def startDependsOnFinishOf(self, t):
        self.dependencies.append(t)

    def conflictsWith(self, t):
        self.conflicts.append(t)

    def is_happy(self):
        for task in self.dependencies:
            if self.start < task.end:
                return False

        for task in self.conflicts:
            if self.start >= task.start and self.start < task.end:
                return False
            if self.end > task.start and self.end <= task.end:
                return False
        return True

    def __repr__(self):
        return "Task(%s)" % (self.duration)

class TestThings(unittest2.TestCase):
    def assertTaskValues(self, task, start, end, duration):
        self.assertEquals(start, task.start)
        self.assertEquals(end, task.end)
        self.assertEquals(duration, task.duration)

    def test_one_task(self):
        s = TaskSolver()
        t = Task(duration=30)
        s.addTask(t)
        solutions = s.resolve()
        self.assertEquals(1, len(solutions))
        self.assertEquals(1, len(solutions[0]))
        self.assertTaskValues(solutions[0][0], 0, 30, 30)

    def test_one_task_different(self):
        s = TaskSolver()
        t = Task(duration=20)
        s.addTask(t)
        solutions = s.resolve()
        self.assertEquals(1, len(solutions))
        self.assertEquals(1, len(solutions[0]))
        self.assertTaskValues(solutions[0][0], 0, 20, 20)

    def test_two_tasks(self):
        s = TaskSolver()
        t1 = Task(duration=20)
        t2 = Task(duration=30)
        s.addTask(t1)
        s.addTask(t2)
        solutions = s.resolve()
        self.assertEquals(1, len(solutions))
        self.assertEquals(2, len(solutions[0]))
        self.assertTaskValues(solutions[0][0], 0, 20, 20)
        self.assertTaskValues(solutions[0][1], 0, 30, 30)

    def test_two_tasks_dependent(self):
        s = TaskSolver()
        t1 = Task(duration=20)
        t2 = Task(duration=30)
        t1.startDependsOnFinishOf(t2)
        s.addTasks(t1, t2)
        solutions = s.resolve()
        self.assertEquals(1, len(solutions))
        self.assertEquals(2, len(solutions[0]))
        self.assertTaskValues(solutions[0][0], 30, 50, 20)
        self.assertTaskValues(solutions[0][1], 0, 30, 30)

    def test_conflicts_with(self):
        s = TaskSolver()
        t1 = Task(duration=10)
        t2 = Task(duration=20)
        t3 = Task(duration=30)
        t3.startDependsOnFinishOf(t2)
        t1.conflictsWith(t2)
        s.addTasks(t1, t2, t3)
        solutions = s.resolve()
        self.assertEquals(1, len(solutions))
        self.assertEquals(3, len(solutions[0]))
        self.assertTaskValues(solutions[0][0], 20, 30, 10)
        self.assertTaskValues(solutions[0][1], 0, 20, 20)
        self.assertTaskValues(solutions[0][2], 20, 50, 30)

    # TODO: two-argument conflicts; task must be before start of arg1 or after end of arg2
