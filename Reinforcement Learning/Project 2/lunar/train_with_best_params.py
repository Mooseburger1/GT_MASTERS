from agent import Agent
import numpy as np
import gym
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import pickle

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()

    env = gym.make('LunarLander-v2')
    np.random.seed(42)
    tf.random.set_seed(42)
    env.seed(42)

    lr = 0.001
    n_games = 700

    gammas = [0.99]
    mem_sizes = [1000000]
    epsilon_decs = [1e-3]

    for gamma in gammas:
        for mem_size in mem_sizes:
            for epsilon_dec in epsilon_decs:
                print('Gamma {} - Mem Size {} - Epsilon Decay {}'.format(gamma,mem_size,epsilon_dec))
                agent = Agent(gamma=gamma, epsilon=1.0, lr=lr, input_dims=env.observation_space.shape, n_actions=env.action_space.n, 
                              mem_size=mem_size, epsilon_dec=epsilon_dec, batch_size=64, epsilon_end=0.01, saveModel='models/best_model.h5')
                scores = []
                avg_scores = []
                eps_history = []
                iter_time = []
                mem_full = []

                for i in range(n_games):
                    start = time.time()
                    done=False
                    score = 0
                    state = env.reset()
                    while not done:
                        action = agent.choose_action(state)
                        state_next, reward, done, info = env.step(action)
                        score+=reward
                        agent.store_memory(state, action, reward, state_next, done)
                        state = state_next
                        agent.train()

                    end = time.time()
                    mem_full.append(agent.memory.mem_cntr)
                    iter_time.append(float(end-start))

                    eps_history.append(agent.epsilon)

                    scores.append(score)

                    avg_score = np.mean(scores[-100:])
                    avg_scores.append(avg_score)
                    print('episode: ', i, 'score %.2f' % score, 'average_score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon)

                print('saving model')
                agent.save_model()
                
                print('saving metrics')
                metrics_data = {'scores':scores,
                                'avg_scores':avg_scores,
                                'eps_history':eps_history,
                                'iter_time':iter_time,
                                'mem_full':mem_full}

                pickle.dump( metrics_data, open('data/best_data.pickle', "wb" ) ) 
                


                
                filename='images/scores/best_scores.png'
                filename2='images/metrics/best_metrics.png'
                x = [i+1 for i in range(n_games)]

                fig, axes = plt.subplots(figsize=(15,8))
                ax = plt.subplot()
                scores_ = ax.plot(x, scores, label='Scores', color='green')
                averages = ax.plot(x, avg_scores, label='Avg Score', color='red', ls='--')

                ax2 = ax.twinx()

                epsil = ax2.plot(x, eps_history, color='purple', label='Epsilon')

                lns = scores_ + averages + epsil
                labs = [l.get_label() for l in lns]
                ax.legend(lns, labs, loc=0)

                ax.grid()
                ax.set_title('Gamma: {}    Memory Size: {}    Epsilon Decay: {}'.format(gamma,mem_size,epsilon_dec))
                ax.set_xlabel('episodes')
                ax.set_ylabel('scores')
                ax2.set_ylabel('epsilon')
                plt.savefig(filename, bbox_inches='tight')
                plt.close()

                fig,axes = plt.subplots(figsize=(15,8))
                ax3=plt.subplot()
                time_ = ax3.plot(x, iter_time, label='Time / Episode', color='purple', ls='--')
                ax4 = ax3.twinx()
                mem_buff = ax4.plot(x, mem_full, label='Memory Buffer', color='orange')

                lns2 = time_ + mem_buff
                labs2 = [l.get_label() for l in lns2]
                ax3.legend(lns2, labs2, loc=0)

                ax3.grid()
                ax3.set_title('Gamma: {}    Memory Size: {}    Epsilon Decay: {}'.format(gamma,mem_size,epsilon_dec))
                ax3.set_xlabel('episodes')
                ax3.set_ylabel('Time / Episode')
                ax4.set_ylabel('Memory Buffer')
                plt.savefig(filename2, bbox_inches='tight')
                plt.close()
        
