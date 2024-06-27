from celery import shared_task
import gym
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run_gym_env(env_name, episodes=1, steps_per_episode=1000):
    try:
        env = gym.make(env_name)
        for episode in range(episodes):
            observation = env.reset()
            for step in range(steps_per_episode):
                env.render()
                action = env.action_space.sample()
                observation, reward, done, _ = env.step(action)
                if done:
                    break
            logger.info(f"Completed episode {episode + 1} of {env_name}")
        env.close()
    except Exception as e:
        logger.error(f"Error running {env_name}: {e}")


@shared_task
def run_acrobot(episodes=1, steps_per_episode=1000):
    run_gym_env('Acrobot-v1', episodes, steps_per_episode)


@shared_task
def run_cartpole(episodes=1, steps_per_episode=1000):
    run_gym_env('CartPole-v1', episodes, steps_per_episode)


@shared_task
def run_mountaincar(episodes=1, steps_per_episode=1000):
    run_gym_env('MountainCar-v0', episodes, steps_per_episode)


@shared_task
def run_mountaincar_continuous(episodes=1, steps_per_episode=1000):
    run_gym_env('MountainCarContinuous-v0', episodes, steps_per_episode)


@shared_task
def run_pendulum(episodes=1, steps_per_episode=1000):
    run_gym_env('Pendulum-v1', episodes, steps_per_episode)


@shared_task
def run_breakout(episodes=1, steps_per_episode=1000):
    run_gym_env('Breakout-v0', episodes, steps_per_episode)


@shared_task
def run_space_invaders(episodes=1, steps_per_episode=1000):
    run_gym_env('SpaceInvaders-v0', episodes, steps_per_episode)
