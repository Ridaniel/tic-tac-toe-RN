from linearDecay import LinearDecaySchedule
from dql import NN
import torch
import random
import numpy as np
from enviroment import enviroments
from botIzi import Bot
import copy


class SwallowQLearner(object):
    def __init__(self, obs_shape, action_shape, simbolo, MAX_NUM_EPISODES, STEPS_PER_EPISODE, learning_rate=0.01, gamma=0.98):
        self.obs_shape = obs_shape
        self.action_shape = action_shape
        self.Q = NN(self.obs_shape, obs_shape+8, self.action_shape, 2)
        self.simbolo = simbolo

        self.learning_rate = learning_rate
        self.gamma = gamma

        self.epsilon_max = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = LinearDecaySchedule(initial_value=self.epsilon_max,
                                                 final_value=self.epsilon_min,
                                                 max_steps=0.5 * MAX_NUM_EPISODES * STEPS_PER_EPISODE)
        self.step_num = 0
        self.policy = self.epsilon_greedy_Q

        # self.memory = ExperienceMemory(capacity = int(1e5))
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def get_action(self, obs):
        return self.policy(obs)

    def epsilon_greedy_Q(self, obs):
        """
        :obs:   Es el estado de la partida antes de jugar
        """
        #self.Q.update(obs.tablero, self.simbolo, obs.widht)
        # Se verfica que el acción de la RN no sea ilegal
        tryAgain = True
        while(tryAgain):
            if random.random() < self.epsilon_decay(self.step_num):
                action = random.choice([a for a in range(self.action_shape)])
                if(obs.tablero[int(action/len(obs.tablero[0]))][int(action % len(obs.tablero[0]))] == 0):
                    tryAgain = False
            else:
                action = self.Q.max()
                tryAgain = False
        # se retorna la acción a tomar
        return action

    def learn(self, obs, action, reward, next_obs, simbol2):
        """
        :obs:       Es el estado de la partida antes de jugar
        :action:    Es la acción tomada por la RN
        :reward:    Es la recompensa que se obtiene por la acción tomada
        :next_obs:  Es el estado de la partida en 
        :simbol2:   Es el simbolo del jugador enemigo
        """
        # En caso de que el juego termine se le da su recompensa según su resultado(Gano, Empato o Perdió)
        if next_obs.done is False:
            temp = self.Q.next(next_obs, self.simbolo, simbol2)
        else:
            temp = next_obs.final(self.simbolo)

        td_target = reward + self.gamma * temp

        td_error = self.Q.output(
        )[action]+self.learning_rate*(td_target-self.Q.output()[action])
        self.Q.backPropagate(action, td_error, 0, 1)

    # def replay_experience(self, batch_size):
    #     """
    #     Vuelve a jugar usando la experiencia aleatoria almacenada
    #     :param batch_size: Tamaño de la muestrsa a tomar de la memoria
    #     :return:
    #     """
    #     experience_batch = self.memory.sample(batch_size)
    #     self.learn_from_batch_experience(experience_batch)

    # def learn_from_batch_experience(self, experiences):
    #     """
    #     Actualiza la red neuronal profunda en base a lo aprendido en el conjunto de experiencias anteriores
    #     :param experiences: fragmento de recuerdos anteriores
    #     :return:
    #     """
    #     batch_xp = Experience(*zip(*experiences))
    #     obs_batch = np.array(batch_xp.obs)
    #     action_batch = np.array(batch_xp.action)
    #     reward_batch = np.array(batch_xp.reward)
    #     next_obs_batch = np.array(batch_xp.next_obs)
    #     done_batch = np.array(batch_xp.done)

        # td_target = reward_batch + ~done_batch * \
        #     np.tile(self.gamma, len(next_obs_batch)) * \
        #     self.Q(next_obs_batch).detach().max(1)[0].data

        # td_target = td_target.to(self.device)
        # action_idx = torch.from_numpy(action_batch).to(self.device)
        # td_error = torch.nn.functional.mse_loss(
        #     self.Q(obs_batch).gather(1, action_idx.view(-1, 1)),
        #     td_target.float().unsqueeze(1))

        # self.Q_optimizer.zero_grad()
        # td_error.mean().backward()
        # self.Q_optimizer.step()

    def exam(self, hight, widht):
        print("Exam")
        # agente2=Bot(1,1)
        obs = enviroments(hight, widht)
        for i in range(int(hight*widht/2)+1):
            if obs.done is True:
                break
            action = self.get_action(obs)
            next_obs = obs.update(action, self.simbolo)
            obs = next_obs
            print("Jugo en la posición ", action)
            print(obs.tablero)
            if obs.done is True:
                break
            action = int(input())   
            # En caso de querer ver como juegan los bots
            #action = agente2.play(obs.tablero)
            next_obs = obs.update(action, 2)
            #print("Jugo en la posición ", action)
            obs = next_obs
            print(obs.tablero)


def train(MAX_NUM_EPISODES, STEPS_PER_EPISODE, hight, widht):
    """
    :MAX_NUM_EPISODES:  Es el número máximo de pruebas para entrenar la RN
    :STEPS_PER_EPISODE: Es el número máximo de pasos por prueba que puede realizar la RN
    :hight:             Número de filas para el tablero del tic tac toe
    :widht:             Número de columnas para el tablero del tic tac toe
    """

    agent = SwallowQLearner(hight*widht+1, hight*widht,
                            1, MAX_NUM_EPISODES, STEPS_PER_EPISODE)
    agente2 = Bot(2,1)
    # agent2 = SwallowQLearner(10, 9, 2)
    first_episode = True
    for episode in range(MAX_NUM_EPISODES):
        obs = enviroments(hight, widht)
        total_reward = 0.0
        for step in range(STEPS_PER_EPISODE):
            tryAgain = True
            while(tryAgain):
                # Jugada del agente
                action = agent.get_action(obs)
                next_obs = obs.update(action, agent.simbolo)
                obstemp = copy.deepcopy(obs)
                obs = copy.deepcopy(next_obs)

                if next_obs.done is False:
                    action2 = agente2.play(next_obs.tablero)
                    next_obs = next_obs.update(action2, agente2.symbol)
                    if next_obs.done is True:
                        total_reward += next_obs.final(agent.simbolo)
                else:
                    total_reward += next_obs.final(agent.simbolo)

                #agent.memory.store(Experience(obs, action, reward, next_obs, done))
                agent.learn(obs, action, obs.reward, next_obs, 1)
                total_reward += obs.reward
                if(obs.reward != -25):
                    tryAgain = False
                    obs = copy.deepcopy(next_obs)
                else:
                    obs = copy.deepcopy(obstemp)

            if obs.done is True:
                if first_episode:
                    max_reward = total_reward
                    first_episode = False

                if total_reward > max_reward:
                    max_reward = total_reward

                print("\nEpisodio#{} finalizado con {} iteraciones. Recompensa = {} , Mejor recompensa = {}".
                      format(episode, step+1, total_reward, max_reward))
                # if agent.memory.get_size()>100:
                #     agent.replay_experience(32)
                break

    resp = "S"
    while(resp == "S"):
        print("Queries jugar contra la RN?: (S,N)")
        resp = input()
        if(resp == "S"):
            agent.exam(hight, widht)
        else:
            print("Prueba terminada")
