## Sahara :o:


|          |            |
| -------- | ---------- |
| title    | Sahara     | 
| status   | 10         |
| section  | DevOps     |
| keywords | DevOps     |



The Sahara product provides users with the capability to provision
data processing frameworks (such as Hadoop, Spark and Storm) on
OpenStack by specifying several parameters such as the version, cluster
topology and hardware node details [@www-openStack]. The solution
allows for fast provisioning of data processing clusters on OpenStack
for development and quality assurance and utilization of unused
computer power from a general purpose OpenStack Iaas
Cloud [@www-Sahara].  Sahara is managed via a REST API with a User
Interface available as part of OpenStack Dashboard.

The Sahara project is a joint collaboration between Hortonworks, Red Hat 
and Mirantis. The reason the Sahara project was pursued by these entities 
was based on the need for agile access to big data. By sitting on top of the 
OpenStack Cloud management platform, Sahara is able to provide managed 
scalability for the various data processing frameworks. In alignment with 
scalability, the elasticity around the clusters(growing or shrinking resources 
as required) is another major advantage when using Sahara to manage and 
deploy clusters [www-fa18-523-88-openstack-sahara-essentials].

The Sahara product is able to communicate with a variety of OpenStack services.

_Some of the main services that Sahara is able to communicate with are:_ [@www-fa18-523-88-openstack-sahara]

* Horizon  (Dashboards)
* Keystone  (Identification)
* Nova  (Computational provisioning)
* Glance  (VM Image storage)
* Swift  (Object Storage) 

_Thru this communication, Sahara is able to provide some unique characteristics such as:_

_**Rapid Provisioning:**_ Deployment of clusters are facilitated by the GUI interface or the 
command line interface [www-fa18-523-88-openstack-sahara-essentials].

_**Centralized Management:**_ Monitoring and controlling clusters from a single management
interface [www-fa18-523-88-openstack-sahara-essentials].

_**Cluster Management:**_ Sahara templating mechanism allows for the starting, stopping, resizing,
scaling and shaping of the cluster ecosystem. This templating feature allows for easily repeatable 
manipulation and creation of a Hadoop/Spark cluster node while eliminating the need to provide any
detailed cluster node setup parameters [www-fa18-523-88-openstack-sahara-essentials].

_**Workload Management:**_ Defining the Elastic Data Processing(the execution and queueing 
of jobs) and how they should work within the cluster. By defining the type of data 
processing jobs that should run across the cluster, Sahara can enable the provisioning
of new clusters on-demand to process these jobs. When said jobs are complete, Sahara can manage
the dismantling of the cluster [www-fa18-523-88-openstack-sahara-essentials].


