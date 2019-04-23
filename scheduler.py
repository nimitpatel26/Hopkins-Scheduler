from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model


class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_shifts, num_weeks, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_shifts = num_shifts
        self._num_weeks = num_weeks
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        self._solution_count += 1
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for w in range(self._num_weeks):
                print('Week #%i' % w)
                for s in range(self._num_shifts):
                    is_working = False
                    for n in range(self._num_nurses):
                        if self.Value(self._shifts[(n, s, w)]):
                            is_working = True
                            print('  Nurse %i works shift %i' % (n, s))
                    if not is_working:
                        print('  Shift {} is vacant.'.format(n))
            print()

    def solution_count(self):
        return self._solution_count

def main():
    # Data.
    num_nurses = 5
    num_shifts = 19
    num_weeks = 4
                
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_weeks = range(num_weeks)
    
    #Nurse #, Shift #, Week # - Start from zero!
    taken_off = [(0, 7, 3), (2, 7, 3), (3, 7, 3), (4, 7, 3), (3, 2, 0), (2, 10, 2), (1, 15, 1)]
    requested = [(1, 4, 2), (2, 6, 3), (0, 0, 0), (3, 12, 1), (4, 16, 0)]
    
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for s in all_shifts:
            for w in all_weeks:
                shifts[(n, s, w)] = model.NewBoolVar('shift_n%is%iw%i' % (n, s, w))

    # Each shift is assigned to exactly one nurse in the schedule period.
    for s in all_shifts:
        for w in all_weeks:
            model.Add(sum(shifts[(n, s, w)] for n in all_nurses) == 1)
          
    # No adjacent shifts for a nurse.
    for n in all_nurses:
        for l in range(num_shifts*num_weeks - 1):
            s = l % num_shifts
            w = l // num_shifts
            sl = (l+1) % num_shifts
            wl = (l+1) // num_shifts
            model.Add(shifts[(n, s, w)] + shifts[(n, sl, wl)] != 2)
        
    # Each nurse must work at least 122 hours per month.
    for n in all_nurses:
        total_hours = sum(((8 * shifts[(n, s, w)]) if s < 15 else (12 * shifts[(n, s, w)])) for s in all_shifts for w in all_weeks)
        model.Add(total_hours >= 122)
        
    # Nurse has taken off, DO NOT schedule.
    for i in taken_off:
        model.Add(shifts[i] == 0)
        
    # Maximize # of honored requested shifts.
    model.Maximize(sum(shifts[i] for i in requested))
    
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    # Display the first solution.
    a_few_solutions = range(2)
    solution_printer = NursesPartialSolutionPrinter(
        shifts, num_nurses, num_shifts, num_weeks, a_few_solutions)
    solver.SolveWithSolutionCallback(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()