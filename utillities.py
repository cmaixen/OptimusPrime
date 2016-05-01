import matplotlib.pyplot as plt
import numpy as np

def map_step_to_index(Step):
    mapping_dict = {'C': 0, 'C#': 1, 'D':2 ,'D#':3 , 'E':4 ,'F':5 ,'F#':6 ,'G':7 , 'G#':8 , 'A':9 , 'A#':10 , 'B': 11}
    return mapping_dict[Step]




def pretty_scatter(values, legend, output):

    scatter_dict = {}

    fig = plt.figure()

    for i in range(len(legend)):
        if legend[i] in scatter_dict:
            scatter_dict[legend[i]].append(values[i])
        else:
            scatter_dict[legend[i]] = [values[i]]

    text = iter(scatter_dict.keys())

    plot_list = []
    for key in scatter_dict.keys():

        X = [x[0] for x in scatter_dict[key]]
        y = [x[1] for x in scatter_dict[key]]

        plot_list.append(plt.scatter(X,y, color=np.random.rand(3) ))

    plt.legend(plot_list,scatter_dict.keys(),scatterpoints=1,
           loc='upper center',
           ncol=5,
           fontsize=5)

    plt.savefig("./plots/" + output)



def extract_useful_features(matrix_set):
    index_set = set()
    print(len(matrix_set[0]))
    for i in range(len(matrix_set[0])):
        for matrix in matrix_set:
            #check if index contributes for a matrix in the set
            if (matrix[i] != 0):
                index_set.add(i)

    #construct new set with useful matrix features
    new_matrix_set = []

    for matrix in matrix_set:
        temp_matrix = []
        for j in index_set:
            temp_matrix.append(matrix[j])
        #add new matrix to solution
        new_matrix_set.append(temp_matrix)
    print("Reducing trainingsset features From " + str(len(matrix_set[0]))+ " To " + str(len(new_matrix_set[0])))
    return new_matrix_set,index_set


def extract_features_of_trainingsset(testset, index_set):
    #construct new set with the right matrix features
    new_matrix_set = []

    for matrix in testset:
        temp_matrix = []
        for j in index_set:
            temp_matrix.append(matrix[j])
        #add new matrix to solution
        new_matrix_set.append(temp_matrix)
    print("Reducing testset features From " + str(len(testset[0])) + " To " + str(len(new_matrix_set[0])))

    return new_matrix_set
