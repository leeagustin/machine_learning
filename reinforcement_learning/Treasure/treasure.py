{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                                \n",
      "Q-table:\n",
      "\n",
      "       left     right\n",
      "0  0.000000  0.004320\n",
      "1  0.000000  0.025005\n",
      "2  0.000030  0.111241\n",
      "3  0.000000  0.368750\n",
      "4  0.027621  0.745813\n",
      "5  0.000000  0.000000\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import time\n",
    "\n",
    "np.random.seed(2)  # reproducible\n",
    "\n",
    "\n",
    "N_STATES = 6   # the length of the 1 dimensional world\n",
    "ACTIONS = ['left', 'right']     # available actions\n",
    "EPSILON = 0.9   # greedy police\n",
    "ALPHA = 0.1     # learning rate\n",
    "GAMMA = 0.9    # discount factor\n",
    "MAX_EPISODES = 13   # maximum episodes\n",
    "FRESH_TIME = 0.3    # fresh time for one move\n",
    "\n",
    "\n",
    "def build_q_table(n_states, actions):\n",
    "    table = pd.DataFrame(\n",
    "        np.zeros((n_states, len(actions))),     # q_table initial values\n",
    "        columns=actions,    # actions's name\n",
    "    )\n",
    "    # print(table)    # show table\n",
    "    return table\n",
    "\n",
    "\n",
    "def choose_action(state, q_table):\n",
    "    # This is how to choose an action\n",
    "    state_actions = q_table.iloc[state, :]\n",
    "    ## So it doesn't get stuck in a loop\n",
    "    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value\n",
    "        action_name = np.random.choice(ACTIONS)\n",
    "    else:   # act greedy\n",
    "        ## Takes the action with the highest weight (from left and right)\n",
    "        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas\n",
    "    return action_name\n",
    "\n",
    "\n",
    "def get_env_feedback(S, A):\n",
    "    # This is how agent will interact with the environment\n",
    "    if A == 'right':    # move right\n",
    "        if S == N_STATES - 2:   # terminate\n",
    "            S_ = 'terminal'\n",
    "            R = 1\n",
    "        else:\n",
    "            S_ = S + 1\n",
    "            R = 0\n",
    "    else:   # move left\n",
    "        R = 0\n",
    "        if S == 0:\n",
    "            S_ = S  # reach the wall\n",
    "        else:\n",
    "            S_ = S - 1\n",
    "    return S_, R\n",
    "\n",
    "\n",
    "def update_env(S, episode, step_counter):\n",
    "    # This is how environment be updated\n",
    "    env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment\n",
    "    if S == 'terminal':\n",
    "        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)\n",
    "        print('\\r{}'.format(interaction), end='')\n",
    "        time.sleep(2)\n",
    "        print('\\r                                ', end='')\n",
    "    else:\n",
    "        env_list[S] = 'o'\n",
    "        interaction = ''.join(env_list)\n",
    "        print('\\r{}'.format(interaction), end='')\n",
    "        time.sleep(FRESH_TIME)\n",
    "\n",
    "\n",
    "def rl():\n",
    "    # main part of RL loop\n",
    "    q_table = build_q_table(N_STATES, ACTIONS)\n",
    "    for episode in range(MAX_EPISODES):\n",
    "        step_counter = 0\n",
    "        S = 0\n",
    "        is_terminated = False\n",
    "        update_env(S, episode, step_counter)\n",
    "        while not is_terminated:\n",
    "\n",
    "            A = choose_action(S, q_table)\n",
    "            S_, R = get_env_feedback(S, A)  # take action & get next state and reward\n",
    "            q_predict = q_table.loc[S, A]\n",
    "            if S_ != 'terminal':\n",
    "                q_target = R + GAMMA * q_table.iloc[S_, :].max()   # next state is not terminal\n",
    "            else:\n",
    "                q_target = R     # next state is terminal\n",
    "                is_terminated = True    # terminate this episode\n",
    "\n",
    "            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update\n",
    "            S = S_  # move to next state\n",
    "\n",
    "            update_env(S, episode, step_counter+1)\n",
    "            step_counter += 1\n",
    "    return q_table\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    q_table = rl()\n",
    "    print('\\r\\nQ-table:\\n')\n",
    "    print(q_table)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'state_actions' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-32-32a756a80726>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mhelp\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mstate_actions\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0midxmax\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m: name 'state_actions' is not defined"
     ]
    }
   ],
   "source": [
    "help(state_actions.idxmax)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
