#!/usr/bin/python3

import chi.lease
import chi.server
import chi.network

chi.set('project_name', 'CHI-221014')
chi.use_site('CHI@Purdue')

net_name = "stbl"
subnet_name = "private-subnet-stbl-0"
router_name = "public_router"

# automatically set up the network
try:
    network = chi.network.get_network(net_name)
except RuntimeError:
    network = chi.network.create_network(net_name)

try:
    subnet = chi.network.get_subnet(subnet_name)
except RuntimeError:
    subnet = chi.network.create_subnet(subnet_name, network['id'], cidr="10.25.32.0/24")

try:
    router = chi.network.get_router(router_name)
except RuntimeError:
    # may get the error: "IpAddressGenerationFailureClient: No more IP addresses available on network"
    router = chi.network.create_router(router_name, "public")
    chi.network.add_subnet_to_router(router['id'], subnet['id'])


# head node lease
head_node = []
chi.lease.add_node_reservation(head_node, resource_properties=["==", "$node_name", "snyder-a001"], count=1)
head_lease = chi.lease.create_lease("CD_Head_Lease", reservations=head_node)

# if the specified node is reserved, lease any node
if head_lease is None:
    head_node = []
    chi.lease.add_node_reservation(head_node, node_type='indyscc_head', count=1)
    head_lease = chi.lease.create_lease("CD_Head_Lease", reservations=head_node)

head_ready = chi.lease.wait_for_active(head_lease['id'])


# compute node lease
compute_nodes = []
chi.lease.add_node_reservation(compute_nodes, count=1, resource_properties=["==", "$node_name", "rice-a470"])
chi.lease.add_node_reservation(compute_nodes, count=1, resource_properties=["==", "$node_name", "rice-a330"])
compute_lease = chi.lease.create_lease("CD_Compute_Lease", reservations=compute_nodes)

# if any of the specified nodes are reserved, lease any nodes
if compute_lease is None:
    compute_nodes = []
    chi.lease.add_node_reservation(compute_nodes, count=2, node_type='indyscc_compute')
    compute_lease = chi.lease.create_lease("CD_Compute_Lease", reservations=compute_nodes)

compute_ready = chi.lease.wait_for_active(compute_lease['id'])

# Project-specific default image. Replace with stock image if not run in our project.
head_image = 'indyscc_head-node'
compute_image = 'indyscc-compute-node'
ssh_key = 'Test_ssh'  # replace with your generated keypair

head = chi.server.create_server(
    "CD_Head",
    reservation_id=chi.lease.get_node_reservation(head_lease['id']),
    image_name=head_image,
    network_name=net_name,
    key_name=ssh_key
)

compute = chi.server.create_server(
    "CD_Compute",
    reservation_id=chi.lease.get_node_reservation(compute_lease['id']),
    image_name=compute_image,
    network_name=net_name,
    key_name=ssh_key
)

head_node_start = chi.server.wait_for_active(head.id)
compute_nodes_start = chi.server.wait_for_active(compute.id)
chi.server.associate_floating_ip(head.id)
