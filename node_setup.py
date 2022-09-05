#!/usr/bin/python3

import chi, chi.lease, chi.server

chi.set('project_name', 'CHI-221014')
chi.use_site('CHI@Purdue')

# head node lease by node_name
head_node = []
chi.lease.add_node_reservation(head_node, resource_properties=["==", "$node_name", "snyder-a003"], count=1)
head_lease = chi.lease.create_lease("CD_Head_Lease", reservations=head_node)
head_ready = chi.lease.wait_for_active(head_lease['id'])

# compute node lease
compute_nodes = []
chi.lease.add_node_reservation(compute_nodes, count=2, node_type="indyscc_compute")
compute_lease = chi.lease.create_lease("CD_Compute_Lease", reservation=compute_nodes)
compute_ready = chi.lease.wait_for_active(compute_lease['id'])

