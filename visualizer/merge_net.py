import glob
from petrinet.PetriNet import PetriNet


def get_multiple_petri_net_files():
    print (glob.glob("../_running_logs/*/petri-net.pkl"))
    return glob.glob("../_running_logs/*/petri-net.pkl")


def load_file() -> PetriNet:
    net_files = get_multiple_petri_net_files()
    merged_net = PetriNet.load(net_files[0])
    if len(net_files) > 1:
        for idx in range(1, len(net_files)):
            merged_net = PetriNet.merge(merged_net, PetriNet.load(net_files[idx]))
    return merged_net


merged_net = load_file()
PetriNet.save(merged_net, "../running_logs/merged_net.pkl")
print("Merged Petri-Net is saved to : ../running_logs/merged_net.pkl")
