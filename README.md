# PythonToDo
A little algorithmic to-do list thing. One part learning project to one part thing I actually think ought to exist.


# Description
This idea comes from reading [Algorithms to Live By - Christian-Griffiths](https://www.amazon.co.uk/dp/B015DLA0LE?ref=KC_GS_GB_GB). Scheduling algorithms are hard, but there are a couple that will give pretty good results on average, particularly in the real world (where uncertainty makes optimal solutions computationally expensive or even impossible). So here's the idea: a to do list which takes simple inputs and automatically prioritises the list, so any time you open up the list you're immediately presented with the next most important task.

# Inputs
- Importance
- Effort required
- (Deadline)
- (Earliest available start) # e.g. renewing an MOT is very important and takes little effort, but can't be started until the existing one is nearly expired
- (Dependencies)

# Algorithm
Weighted shortest remaining time (importance / time to complete)

# MVP
- Can add/edit/remove/complete list items with name, importance, and effort
- On any of the above changes to the list, a priority order is calculated
- List is displayed in priority order

# Features (eventually, maybe)
- Support for deadlines and earliest available start dates.
- Default values for importance, effort, and deadline (e.g. one week from now)
- Precedence constraints (and priority inheritance)
	- A low priority task which blocks a high priority task should become high priority. "If you're flammable and have legs, you're never blocking the fire exit" -Mitch Hedberg
- Multi-device support, phone/PC apps, cloud backup

## Task hierarchies

If one task is too big to practically deal with as one item, should be able to split it into several related tasks.

**Questions**
-  Will priority for all tasks will evaluated together?
	- Take the highest single priority?
	- Average weighting across all individual tasks?
- Is value for all tasks only realised when the whole block is complete?
	- If so, task group is effectively a single task from the app's perspective - division is really just for human reading.

## Calendar scheduling

With a parameter for available time per day, and a prioritised list of tasks, we can automatically schedule tasks to give an estimate of when a given thing will be completed.

Obviously, this is also heavily impacted by dependencies, deadlines, and earliest possible start dates.

Also feel that my to do list should never tell me off: if I deviate from the plan in any way, it should just accept the new reality and compute accordingly. No failure state, tasks just roll over and reprioritise as necessary to ensure no missed deadlines. Perhaps a warning if there's no way to meet a deadline within the current constraints?

**Questions**
- Do we allow for different available time on different days?
- Do we let a single task be split across multiple days?
- Is daily scheduling unnecessarily, misleadingly precise? Could schedule by week.

Potentially we could answer all these questions by making them configurable by the user (probably just at a global level, though could potentially set a default for whether tasks can split across days and then allow individual tasks to deviate from that).
