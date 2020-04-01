from aux_functions import *
from configs.read_cfg import read_cfg
import importlib, json
from unreal_envs.initial_positions import *
# from aux_functions import *
# TF Debug message suppressed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



def generate_json(cfg):
    flag  = True
    path = os.path.expanduser('~\Documents\Airsim')
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + '\settings.json'

    data = {}

    if cfg.mode == 'move_around':
        data['SimMode'] = 'ComputerVision'
    else:
        data['SettingsVersion'] = 1.2
        data['LocalHostIp'] = cfg.ip_address
        data['SimMode'] = cfg.SimMode
        data['ClockSpeed'] = cfg.ClockSpeed
        data["ViewMode"]= "NoDisplay"
        PawnPaths = {}
        PawnPaths["DefaultQuadrotor"] = {}
        PawnPaths["DefaultQuadrotor"]['PawnBP'] = ''' Class'/AirSim/Blueprints/BP_''' + cfg.drone + '''.BP_''' + cfg.drone + '''_C' '''
        data['PawnPaths']=PawnPaths

        # Define agents:
        _, reset_array_raw, _, _ = initial_positions(cfg.env_name, num_agents=cfg.num_agents)
        Vehicles = {}
        if len(reset_array_raw) < cfg.num_agents:
            print("Error: Either reduce the number of agents or add more initial positions")
            flag = False
        else:
            for agents in range(cfg.num_agents):
                name_agent = "drone" + str(agents)
                agent_position = reset_array_raw[name_agent].pop(0)
                Vehicles[name_agent] = {}
                Vehicles[name_agent]["VehicleType"] = "SimpleFlight"
                Vehicles[name_agent]["X"] = agent_position[0]
                Vehicles[name_agent]["Y"] = agent_position[1]
                # Vehicles[name_agent]["Z"] = agent_position[2]
                Vehicles[name_agent]["Z"] = 0
                Vehicles[name_agent]["Yaw"] = agent_position[3]
            data["Vehicles"] = Vehicles

        CameraDefaults = {}
        CameraDefaults['CaptureSettings']=[]
        # CaptureSettings=[]1

        camera = {}
        camera['ImageType'] = 0
        camera['Width'] = cfg.width
        camera['Height'] = cfg.height
        camera['FOV_Degrees'] = cfg.fov_degrees

        CameraDefaults['CaptureSettings'].append(camera)

        camera = {}
        camera['ImageType'] = 3
        camera['Width'] = cfg.width
        camera['Height'] = cfg.height
        camera['FOV_Degrees'] = cfg.fov_degrees

        CameraDefaults['CaptureSettings'].append(camera)

        data['CameraDefaults'] = CameraDefaults
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return flag


if __name__ == '__main__':
    # Read the config file
    cfg = read_cfg(config_filename='configs/config.cfg', verbose=True)
    can_proceed = generate_json(cfg)
    if can_proceed:
        algorithm = importlib.import_module('algorithms.'+cfg.algorithm)
        name = 'algorithm.' + cfg.algorithm + '(cfg)'
        eval(name)





