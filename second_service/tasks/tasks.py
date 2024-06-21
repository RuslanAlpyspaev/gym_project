from celery import shared_task
import gym


@shared_task
def run_acrobot():
    env = gym.make('Acrobot-v1')
    observation = env.reset()
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
    env.close()


@shared_task
def run_cartpole():
    env = gym.make('CartPole-v1')
    observation = env.reset()
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
    env.close()


@shared_task
def run_mountaincar():
    env = gym.make('MountainCar-v0')
    observation = env.reset()
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
    env.close()


@shared_task
def run_mountaincar_continuous():
    env = gym.make('MountainCarContinuous-v0')
    observation = env.reset()
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
    env.close()


@shared_task
def run_pendulum():
    env = gym.make('Pendulum-v1')
    observation = env.reset()
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
    env.close()
