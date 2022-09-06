#!/usr/bin/python3

import chi, chi.lease, chi.server, chi.network

chi.set('project_name', 'CHI-221014')
chi.use_site('CHI@Purdue')

# set up the network outside the ClusDur project
stbl_net = chi.network.create_network("stbl")
subnet = chi.network.create_subnet("private-subnet-stbl-0", chi.network.get_network_id("stbl"))
router = chi.network.create_router("public_router")
chi.network.add_subnet_to_router(chi.network.get_router_id("public_router"), chi.network.get_subnet_id("private-subnet-stbl-0"))

# head node lease by node_name
head_node = []
chi.lease.add_node_reservation(head_node, resource_properties=["==", "$node_name", "snyder-a003"], count=1)
head_lease = chi.lease.create_lease("CD_Head_Lease", reservations=head_node)
head_ready = chi.lease.wait_for_active(head_lease['id'])

# compute node lease by node_name
compute_nodes = []
chi.lease.add_node_reservation(compute_nodes, count=1, resource_properties=["==", "$node_name", "rice-a443"])
chi.lease.add_node_reservation(compute_nodes, count=1, resource_properties=["==", "$node_name", "rice-a447"])
compute_lease = chi.lease.create_lease("CD_Compute_Lease", reservation=compute_nodes)
compute_ready = chi.lease.wait_for_active(compute_lease['id'])

# outside the ClusDur project replace the image_name and key_name with a stock image and a generated keypair respectively.

head = chi.server.create_server(
    "CD_Head",
    reservation_id=chi.lease.get_node_reservation(head_lease['id']),
    image_name='indyscc_head-node',
    network_name='stbl',
    key_name="Test_ssh"
)

compute = chi.server.create_server(
    "CD_Compute",
    reservation_id=chi.lease.get_node_reservation(compute_lease['id']),
    image_name='indyscc_head-node',
    network_name='stbl',
    key_name="Test_ssh"
)

hserv_start = chi.server.wait_for_active(head.id)
cserv_start = chi.server.wait_for_active(compute.id)
chi.server.associate_floating_ip(head.id)