import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''

    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_offtrack = params['is_offtrack']

    # Initialize the reward
    reward = 1e-3

    # Reward if the agent is on the track
    if all_wheels_on_track:
        reward = 1.0

    if is_offtrack:
        reward = 1e-3

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Calculate the direction of the center line based on the closest waypoints
    nextPoint = waypoints[closest_waypoints[1]]
    prevPoint = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius
    trackDirection = math.degrees(math.atan2(nextPoint[1] - prevPoint[1], nextPoint[0] - prevPoint[0]))

    # Calculate the difference between the track direction and the heading direction the car
    directionDifference = abs(trackDirection - heading)
    if directionDifference > 180:
        directionDifference = 360 - directionDifference

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if directionDifference > DIRECTION_THRESHOLD:
        reward *= 0.5

    return float(reward)