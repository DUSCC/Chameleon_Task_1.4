#!/usr/bin/python3

import chi, chi.lease, chi.server

chi.set('project_name', 'CHI-221014')
chi.use_site('CHI@Purdue')

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

# ASSUME THE ISOLATED NETWORK AND ROUTER HAVE BEEN SET UP IN THE GUI
head = chi.server.create_server(
    "CD_Head",
    reservation_id=chi.lease.get_node_reservation(head_lease['id']),
    image_name='CC-Ubuntu20.04',
    network_name='stbl'
)

compute = chi.server.create_server(
    "CD_Compute",
    reservation_id=chi.lease.get_node_reservation(compute_lease['id']),
    image_name='CC-Ubuntu20.04',
    network_name='stbl'
)

serv_start = chi.server.wait_for_active(head_node['id'])
chi.server.associate_floating_ip(head_node['id'])