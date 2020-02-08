import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from training_set_generator import walkGenerator
from td_lambda import experiment_2





if __name__ == '__main__':

    alphas = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    generated_sets = walkGenerator().generate_training_sets(num_samples=100, sequences_per_sample=10)

    point_zero = []
    point_one = []
    point_two = []
    point_three = []
    point_four = []
    point_five = []
    point_six = []
    point_seven = []
    point_eight = []
    point_nine = []
    one = []
    print('Running Experiment.......One Moment Please')
    for i in range(len(generated_sets)):
        vs8 = experiment_2(generated_sets[i], lamda=0.8, gamma=1, alphas=alphas)
        vs1 = experiment_2(generated_sets[i], lamda=1.0, gamma=1, alphas=alphas)
        vs3 = experiment_2(generated_sets[i], lamda=0.3, gamma=1, alphas=alphas)
        vs0 = experiment_2(generated_sets[i], lamda=0.0, gamma=1, alphas=alphas)

        vs01 = experiment_2(generated_sets[i], lamda=0.1, gamma=1, alphas=alphas)
        vs2 = experiment_2(generated_sets[i], lamda=0.2, gamma=1, alphas=alphas)
        vs4 = experiment_2(generated_sets[i], lamda=0.4, gamma=1, alphas=alphas)
        vs5 = experiment_2(generated_sets[i], lamda=0.5, gamma=1, alphas=alphas)
        vs6 = experiment_2(generated_sets[i], lamda=0.6, gamma=1, alphas=alphas)
        vs7 = experiment_2(generated_sets[i], lamda=0.7, gamma=1, alphas=alphas)
        vs9 = experiment_2(generated_sets[i], lamda=0.9, gamma=1, alphas=alphas)


        
        point_eight.append(vs8)
        one.append(vs1)
        point_three.append(vs3)
        point_zero.append(vs0)

        point_one.append(vs01)
        point_two.append(vs2)
        point_four.append(vs4)
        point_five.append(vs5)
        point_six.append(vs6)
        point_seven.append(vs7)
        point_nine.append(vs9)
        
    point_zero = np.mean(point_zero, axis=0)
    point_three = np.mean(point_three, axis=0)
    point_eight = np.mean(point_eight, axis=0)
    one = np.mean(one, axis=0)

    point_one= np.mean(point_one, axis=0)
    point_two= np.mean(point_two, axis=0)
    point_four= np.mean(point_four, axis=0)
    point_five= np.mean(point_five, axis=0)
    point_six= np.mean(point_six, axis=0)
    point_seven= np.mean(point_seven, axis=0)
    point_nine= np.mean(point_nine, axis=0)

    #lowest error for each lambda
    low_zero_idx = np.argmin(point_zero)
    low_three_idx = np.argmin(point_three)
    low_eight_idx = np.argmin(point_eight)
    low_one_idx = np.argmin(one)

    low_pone_idx = np.argmin(point_one)
    low_two_idx = np.argmin(point_two)
    low_four_idx = np.argmin(point_four)
    low_five_idx = np.argmin(point_five)
    low_six_idx = np.argmin(point_six)
    low_seven_idx = np.argmin(point_seven)
    low_nine_idx = np.argmin(point_nine)

    lam = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    lowest_err = (point_zero[low_zero_idx],
                  point_one[low_pone_idx],
                  point_two[low_two_idx],
                  point_three[low_three_idx],
                  point_four[low_four_idx],
                  point_five[low_five_idx],
                  point_six[low_six_idx],
                  point_seven[low_seven_idx],
                  point_eight[low_eight_idx],
                  point_nine[low_nine_idx],
                  one[low_one_idx])

    plt.figure(figsize=(15,8))
    plt.plot(alphas, point_zero, color='red', marker='o', label = 'λ = 0.0', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
    plt.plot(alphas, point_three, color='green', marker='o', label = 'λ = 0.3', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
    plt.plot(alphas, point_eight, color='blue', marker='o', label= 'λ = 0.8', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
    plt.plot(alphas, one, color='orange', marker='o', label='λ = 1.0', path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
    plt.xlabel(chr(945))
    plt.ylabel('RMSE')
    plt.title('SCOTT SIMS FIGURE 4 REPLICATION', fontsize=50)
    plt.ylim(0,1.0)
    plt.legend()
    plt.show()


    plt.figure(figsize=(15,8))
    plt.plot(lam, lowest_err, marker='o',path_effects=[pe.Stroke(linewidth=2, foreground='k'), pe.Normal()])
    plt.xlabel('λ')
    plt.ylabel('Error Using Best {}'.format(chr(945)))
    plt.show()