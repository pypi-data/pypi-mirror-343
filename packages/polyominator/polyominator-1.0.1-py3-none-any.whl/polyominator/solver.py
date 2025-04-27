import numpy as np
import pandas as pd
from scipy.ndimage import correlate
from algorithm_x import AlgorithmX

class polyomino:
    def __init__(self,figures: list[np.ndarray[bool]],area: np.ndarray[bool],is_rotate=True):
        self.figures = figures
        self.area = np.array(area).astype('float')
        self.rotates = [90*i for i in range((4 if is_rotate else 1))]
        self.columns = pd.MultiIndex.from_tuples(
            [('Figures',i) for i in range(len(figures))]
            + [('Cells',i,j) for i,j in zip(*self.area.nonzero())]
        )
        # self._df_algorithm_X_matrix = pd.DataFrame(columns=self.columns)

    def solve(self,get_only_one_solve=True):
        solver_len = len(self.columns)
        solver = AlgorithmX(solver_len)
        #Перебрать фигуры
        for figure_idx, figure in enumerate(self.figures):
            #Найти все их вариации
            figure_variable = self.get_figure_variables(figure)
            for rotate_idx, variable in enumerate(figure_variable):
                # Найти возможные положения
                places = self.get_all_possible_places_for_figure(variable,self.area)
                for place_idx, place in enumerate(places):
                    #Преобразовать фигур-повороты и их возможны расположения в строку для Алгоритма Х
                    indeces_of_closed_cells = self.get_row_for_algorithm_x(figure_idx,place)
                    # ic(indeces_of_closed_cells)
                    solver.appendRow(indeces_of_closed_cells,tag=(figure_idx,rotate_idx,place))
        #Провести алгоритм Х
        solutions = solver.solve()
        #Преобразовать результаты алгоритма Х в понятный вид
        sweet_solutions = (self.get_sweet_solution(solution) for solution in solutions)
        #Вывести результаты
        if get_only_one_solve:
            return next(sweet_solutions)
        else:
            return sweet_solutions

    def get_figure_variables(self,figure):
        rotate_counts = list(range(len(self.rotates)))
        variables = get_rotates(figure,rotate_counts).values()
        return variables
    
    def get_all_possible_places_for_figure(self,figure,area):
        figure = np.array(figure)
        area = np.array(area)

        kernel = make_array_as_kernel(figure)
        origin = -(np.array(kernel.shape) // 2)
        figure_area_correlate = correlate(area,kernel,mode='constant',cval=0,origin=origin)

        element_in_figure = figure.sum()
        possible_places_anchor = (figure_area_correlate == element_in_figure).nonzero()
        figure_nonzero = figure.nonzero()
        possible_places = [np.array(figure_nonzero).T + np.array(row_col) for row_col in zip(*possible_places_anchor)] 

        return possible_places
    
    def get_row_for_algorithm_x(self,figure_idx,place):
        local_columns = pd.MultiIndex.from_tuples(
            [('Figures',figure_idx)]
            + [('Cells',int(i),int(j)) for i,j in place]
        )
        ones = np.ones(len(local_columns))
        place_variant = pd.DataFrame(columns=self.columns,data=pd.DataFrame([ones],columns=local_columns)).T
        indeces = np.arange(len(self.columns))
        is_cell_closed = ~place_variant.isna()[0].to_numpy()
        indeces_of_closed_cells = indeces[is_cell_closed]
        return indeces_of_closed_cells
    
    def get_sweet_solution(self,solution: list[int,int,np.ndarray]):
        #TODO: Добавить сюда сырое решение
        return self.get_masked_area_from_solution(solution)
    
    def get_masked_area_from_solution(self,solution: list[int,int,np.ndarray]):
        area = np.empty_like(self.area)
        area[:] = np.nan
        for figure in solution:
            figure_idx = figure[0]
            figure_loc = figure[2]
            for coord in figure_loc:
                area[*coord] = figure_idx
        return np.array(area,dtype=int)

def get_rotates(figure,rotate_counts=[0,1,2,3]):
    figure = np.array(figure)
    rotates = {90*k: np.rot90(figure,k=k) for k in rotate_counts}
    return rotates

def make_array_as_kernel(array):
    array = np.array(array)
    rows, cols = array.shape
    max_dim = max(rows, cols)
    final_dim = max_dim if max_dim % 2 == 1 else max_dim + 1
    pad_rows, pad_cols = final_dim - rows, final_dim - cols
    return np.pad(array, ((0, pad_rows), (0, pad_cols)), mode='constant', constant_values=0)


def main():
    area = np.ones((6,4))
    # ic(area)

    figures = [
        np.array([
            [1,1,1,1]
        ])
        ,np.array([
            [1,1]
            ,[1,1]
        ])
        ,np.array([
            [1,1,1]
            ,[0,1,0]
        ])
        ,np.array([
            [1,1,1]
            ,[0,1,0]
        ])
        ,np.array([
            [1,1,1]
            ,[1,0,0]
        ])
        ,np.array([
            [1,1,0]
            ,[0,1,1]
        ])
    ]


    pm = polyomino(figures,area)
    # print(pm.df_algorithm_X_matrix)
    solutions = pm.solve(False)
    for solution in solutions:
        print(solution)

if __name__=='__main__':
    main()