import numpy as np


def zero_value(env):
    """
    Returns a zeroed numpy ndarray with size: (|S|, |A|).
    """
    # Size of Value Array: (nS, nA)
    size = (env.nS, env.nA)
    return np.zeros(size)


def egreedy_policy(s, Q, epsilon):
    """
    Given a policy Q and a state s, return an action from Q chosen with e-greedy
    policy. Such action is chosen greedily with probability 1-epsilon.
    """
    # Obtain random number in range [0,1)
    random = np.random.rand()
    # If random in epsilon, choose random action
    if random < epsilon:
        num_actions = Q[s].shape[0]
        indices = np.arange(num_actions)
        return np.random.choice(indices)
    # Otherwise return greedy action
    return np.argmax(Q[s])


def sarsa(env, alpha=0.5, gamma=1, epsilon=.1, num_episodes=200):
    """
    Returns the Q-value estimates for an environment by using the SARSA
    algorithm (State-Action-Reward-State-Action).

    Parameters
    ----------
    env : gym.core.Env
        OpenAI Gym Environment instance
    alpha : float
        Algorithm's learning rate
    gamma : float
        Discount for next rewards
    epsilon : float
        Probability of choosing an action randomly
    num_episodes : int
        Number of episodes for the policy iteration process

    Returns
    -------
    numpy.ndarray
        Estimated Q (state-action) values
    list
        List of rewards of each episode

    """
    # Stats tracking
    sum_rewards = []
    # Create Q
    Q = zero_value(env)
    # Run for a given number of times
    for t in range(num_episodes):
        sum_rewards.append(0)
        # Obtain initial state
        state = env.reset()
        # Choose action from env given e-greedy policy given Q
        action = egreedy_policy(state, Q, epsilon)
        # Run each episode
        while True:
            # Take action, obtain next state & reward
            next_state, reward, done, _ = env.step(action)
            # Choose next action
            next_action = egreedy_policy(next_state, Q, epsilon)
            # Approximate Q
            Q[state][action] += alpha * \
                (reward + gamma * Q[next_state]
                 [next_action] - Q[state, action])
            # Update state variables
            state = next_state
            action = next_action
            sum_rewards[t] += reward
            # Finish episode if done==True
            if done:
                break
    return Q, sum_rewards


def qlearning(env, alpha=0.5, gamma=1, epsilon=0.1, num_episodes=100):
    """
    Returns the Q-value estimates for an environment by using the Q-Learning
    algorithm.

    Parameters
    ----------
    env : gym.core.Env
        OpenAI Gym Environment instance
    alpha : float
        Algorithm's learning rate
    gamma : float
        Discount for next rewards
    epsilon : float
        Probability of choosing an action randomly
    num_episodes : int
        Number of episodes for the policy iteration process

    Returns
    -------
    numpy.ndarray
        Estimated Q (state-action) values
    list
        List of rewards of each episode

    """
    # Stats tracking
    sum_rewards = []
    # Create Q
    Q = zero_value(env)
    # Run for a given number of times
    for t in range(num_episodes):
        sum_rewards.append(0)
        # Obtain initial state
        state = env.reset()
        # Run each episode
        while True:
            # Choose action from env given e-greedy policy given Q
            action = egreedy_policy(state, Q, epsilon)
            # Take action, obtain next state & reward
            next_state, reward, done, _ = env.step(action)
            # Choose next action as max Q(S',a) or equivalently max(Q[s'])
            next_action = np.argmax(Q[next_state])
            # Approximate Q
            Q[state][action] += alpha * \
                (reward + gamma * Q[next_state]
                 [next_action] - Q[state][action])
            # Update state variable
            state = next_state
            sum_rewards[t] += reward
            # Finish episode if done==True
            if done:
                break
    return Q, sum_rewards


def double_qlearning(env, alpha=0.5, gamma=1, epsilon=0.1, num_episodes=100):
    """
    Returns the Q-value estimates for an environment by using the Double
    Q-Learning algorithm.

    Parameters
    ----------
    env : gym.core.Env
        OpenAI Gym Environment instance
    alpha : float
        Algorithm's learning rate
    gamma : float
        Discount for next rewards
    epsilon : float
        Probability of choosing an action randomly
    num_episodes : int
        Number of episodes for the policy iteration process

    Returns
    -------
    numpy.ndarray
        Estimated Q (state-action) values
    list
        List of rewards of each episode

    """
    # Stats tracking
    sum_rewards = []
    # Create Q1 and Q2
    Q1 = zero_value(env)
    Q2 = zero_value(env)
    # Run for a given number of times
    for t in range(num_episodes):
        sum_rewards.append(0)
        # Obtain initial state
        state = env.reset()
        # Run each episode
        while True:
            # Choose action from env given e-greedy policy given Q1 and Q2
            action = egreedy_policy(state, Q1 + Q2, epsilon)
            # Take action, obtain next state & reward
            next_state, reward, done, _ = env.step(action)
            # Choose policy to update randomly
            if np.random.rand() < .5:
                # Choose next action as max Q(S',a) or equivalently max(Q[s'])
                next_action = np.argmax(Q1[next_state])
                # Approximate Q
                Q1[state][action] += alpha * \
                    (reward + gamma * Q2[next_state]
                     [next_action] - Q1[state][action])
            else:
                # Choose next action as max Q(S',a) or equivalently max(Q[s'])
                next_action = np.argmax(Q2[next_state])
                # Approximate Q
                Q2[state][action] += alpha * \
                    (reward + gamma * Q1[next_state]
                     [next_action] - Q2[state][action])
            # Update state variable
            state = next_state
            sum_rewards[t] += reward
            # Finish episode if done==True
            if done:
                break
    return (Q1 + Q2) / 2, sum_rewards
