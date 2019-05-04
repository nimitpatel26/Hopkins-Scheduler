from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model
import itertools

class Shift:
    def __init__(self, startTime, endTime):
        self._startTime = startTime
        self._endTime = endTime
        
    def setShift(self, startEnd):
        self._startTime = startEnd[0]
        self._endTime = startEnd[1]
        
    def getShift(self):
        return (self._startTime, self._endTime)
        
    def getMinuteLength(self):
        hourEnd = self._endTime // 100
        minuteEnd = self._endTime % 100
        hourStart = self._startTime // 100
        minuteStart = self._startTime % 100
        
        endValue = hourEnd * 60 + minuteEnd
        startValue = hourStart * 60 + minuteStart
        
        if startValue >= endValue:
            endValue += 1440
        
        return endValue - startValue
        
class Day:
    def __init__(self, shiftObjectList):
        self._shiftObjectList = shiftObjectList
    
    def setDayShifts(self, shiftList):
        self._shiftList = shiftList
    
    
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_hours, nurse_names, nurse_num, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_hours = num_hours
        self._nurse_names = nurse_names
        self._nurse_num = nurse_num
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % (self._solution_count + 1))
            print('===========')
            for d in range(self._num_days):
                print('Day #%i' % d)
                for h in range(self._num_hours):
                    is_working = False
                    for n in range(self._num_nurses):
                        if self.Value(self._shifts[(n, d, h)]):
                            is_working = True
                            print('  %02i:00 - %s' % (h, self._nurse_names[self._nurse_num[n]]))
                    if not is_working:
                        print('  Shift {} is vacant.'.format(n))
            print()
            self._solution_count += 1

    def solution_count(self):
        return self._solution_count

def main():
    # Data.
    
    nurse_names = ['Jefferson Steelflex', 'Robert Yakatori', 'Anne Parker', 'Sam Greenwich', 'PRN']
    nurses = [[10], [9], [10], [8], [8, 10]]
    nurse_req_hours = [[40, 40], [36, 36], [30, 30], [24, 24], [0, 10000000000000]]
    
    num_days = 7
    num_hours = 24
    
    #Nurse #, Day #, Hour # - Start from zero. For shift_start, it's just day and hour #.
    must_off = []
    requested_off = []
    requested_on = []
    shift_start = []
    
    nurse_corr = [] 
    nurse_num = []
    nurse_hours = []
    
    counter = 0
    counter_2 = 0
    for i in nurses:
        a = []
        for j in i:
            a.append(counter)
            counter = counter + 1
            nurse_num.append(counter_2)
            nurse_hours.append(j)
        nurse_corr.append(a)
        counter_2 = counter_2 + 1
    
    print(nurse_corr)
    print(nurse_num)
    print(nurse_hours)
    
    num_nurses = len(nurse_hours)
                
    all_nurses = range(num_nurses)
    all_days = range(num_days)
    all_hours = range(num_hours)
    
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works day 'd' on hour 'h'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for h in all_hours:
                shifts[(n, d, h)] = model.NewBoolVar('hour_n%id%ih%i' % (n, d, h))

    # Each shift is assigned to exactly one nurse in the schedule period.
    for d in all_days:
        for h in all_hours:
            model.Add(sum(shifts[(n, d, h)] for n in all_nurses) == 1)
          
    # No adjacent shifts for a nurse.
    """
    for n in all_nurses:
        for l in range(num_shifts*num_weeks - 1):
            s = l % num_shifts
            w = l // num_shifts
            sl = (l+1) % num_shifts
            wl = (l+1) // num_shifts
            model.Add(shifts[(n, s, w)] + shifts[(n, sl, wl)] != 2)
    """
    # Adjacent bits per block size, no adjacent blocks! Be sure to add code to handle edges. - DONE
    
    for n in all_nurses:
        block = nurse_hours[n]
        if block != 1:
            for l in range(block - 1, num_days*num_hours - block + 1):
                hours_imp = []
                for i in range(l - block + 1, l + block):
                    hours_imp.append(tuple([n, i // num_hours, i % num_hours]))
                model.Add(sum(shifts[i] for i in hours_imp) == block).OnlyEnforceIf(shifts[hours_imp[block - 1]])
                
            for smaller_block in range(block - 1):
                hours_imp = []
                for i in range(smaller_block + 1):
                    hours_imp.append(tuple([n, i // num_hours, i % num_hours]))
                model.Add(sum(shifts[i] for i in hours_imp) == smaller_block + 1).OnlyEnforceIf(shifts[hours_imp[smaller_block]])
                
            for smaller_block in range(num_days*num_hours - block + 1, num_days*num_hours):
                hours_imp = []
                for i in range(smaller_block, num_days*num_hours):
                    hours_imp.append(tuple([n, i // num_hours, i % num_hours]))
                model.Add(sum(shifts[i] for i in hours_imp) == (num_days*num_hours - smaller_block)).OnlyEnforceIf(shifts[hours_imp[0]])
                
        else:
            for l in range(num_days*num_hours - 1):
                hours_imp = []
                for i in range(l, l + 2):
                    hours_imp.append(tuple([n, i // num_hours, i % num_hours]))
                model.Add(sum(shifts[i] for i in hours_imp) != 2)
            """
            - Old Code
            s = l % num_shifts
            w = l // num_shifts
            sl = (l+1) % num_shifts
            wl = (l+1) // num_shifts
            sn = (l-1) % num_shifts
            wn = (l-1) // num_shifts
            sl2 = (l+2) % num_shifts
            wl2 = (l+2) // num_shifts
            sn2 = (l-2) % num_shifts
            wn2 = (l-2) // num_shifts
           
            - For n block attempts
            
            model.AddBoolOr([shifts[(n, sl, wl)]  shifts[(n, sn, wn)].Not(), shifts[(n, sl, wl)].Not() and shifts[(n, sn, wn)]]).OnlyEnforceIf(shifts[n, s, w])
            
            - The basis
            
            a and !b
            or
            !a and b
            ---------
            a or b
            and
            !a or !b
            ==========
            !a and !b and c and d
            or
            !a and b and c and !d
            or
            a and b and !c and !d

            - more Attempts
            
            num = 2 ** 4
            
            for i in range(num):
                model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            
            
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)], shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)], shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)], shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)].Not(), shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)], shifts[(n, sl2, wl2)].Not(), shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)], shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)], shifts[(n, sl2, wl2)], shifts[(n, sn2, wn2)]]).OnlyEnforceIf(shifts[(n, s, w)])
            
            - Extend for 3 blocks, second line fails
            model.Add(shifts[(n, sn2, wn2)] + shifts[(n, sn, wn)] + shifts[(n, sl, wl)] + shifts[(n, sl2, wl2)] == 2).OnlyEnforceIf(shifts[n, s, w])
            model.Add(((4 * shifts[(n, sn2, wn2)]) - (3 * shifts[(n, sn, wn)]) - (2 * shifts[(n, sl, wl)]) - (1 * shifts[(n, sl2, wl2)])) == 1).OnlyEnforceIf(shifts[n, s, w])
                
            - XOR for 2 blocks, both methods work
            model.AddBoolOr([shifts[(n, sl, wl)], shifts[(n, sn, wn)]]).OnlyEnforceIf(shifts[(n, s, w)])
            model.AddBoolOr([shifts[(n, sl, wl)].Not(), shifts[(n, sn, wn)].Not()]).OnlyEnforceIf(shifts[(n, s, w)])
            
            model.Add(shifts[(n, sl, wl)] + shifts[(n, sn, wn)] == 1).OnlyEnforceIf(shifts[n, s, w])
            """
    
    # A nurse must start/end a shift at this time. - DONE
    
    for s in shift_start:
        num = s[0] * num_hours + s[1]
        prev = num - 1
        prev_d = prev // num_hours
        prev_h = prev % num_hours
        
        for n in all_nurses:
            model.Add(shifts[(n, s[0], s[1])] + shifts[(n, prev_d, prev_h)] != 2)
        
    # Each nurse must start work for a certain # of evenings. (IN PROGRESS)
    """
    for n in all_nurses:
        total_evenings = sum(shifts[(n, d, h)] + shifts[(n, d, h - 1)].Not() for d in all_days for h in range(3, 6))
      
        #total_evenings = sum((shifts[(n, l // num_hours, l % num_hours)].Not() + shifts[(n, (l+1) // num_hours, (l+1) % num_hours)] == 2) if ((l+1) % num_hours > 2 and (l+1) % num_hours < 6) else 0 for l in range(num_days*num_hours - 1))
        model.Add(total_evenings >= 2)
    """
    # Don't let "same" nurses work next to each other. - DONE
    for n in range(num_days*num_hours - 1):
        for i in nurse_corr:
            for j, k in itertools.permutations(i, 2):
                if n == 0:
                    print(str(j) + " " + str(k))
                model.Add(shifts[j, n // num_hours, n % num_hours] + shifts[k, (n+1) // num_hours, (n+1) % num_hours] != 2)
        
    # Each nurse must work at least 122 hours per month. - DONE
    counter = 0
    for j in nurse_corr:
        total_hours = sum(shifts[(n, d, h)] for n in j for d in all_days for h in all_hours)
        model.Add(total_hours >= nurse_req_hours[counter][0])
        model.Add(total_hours <= nurse_req_hours[counter][1])
        counter = counter + 1
        
    # Nurse has taken off, DO NOT schedule. - DONE
    
    for i in must_off:
        for j in nurse_corr[i[0]]:
            model.Add(shifts[(j, i[1], i[2])] == 0)
        
    # Maximize # of honored requested on/off shifts. - DONE
    model.Maximize(sum(shifts[j, i[1], i[2]] for i in requested_on for j in nurse_corr[i[0]]) + sum(shifts[j, i[1], i[2]].Not() for i in requested_off for j in nurse_corr[i[0]]))
    
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    # Display the first solution.
    a_few_solutions = range(1)
    solution_printer = NursesPartialSolutionPrinter(
        shifts, num_nurses, num_days, num_hours, nurse_names, nurse_num, a_few_solutions)
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