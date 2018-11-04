## Sahara :o:


|          |            |
| -------- | ---------- |
| title    | Sahara     | 
| status   | 10         |
| section  | DevOps     |
| keywords | DevOps     |



The Sahara product provides users with the capability to provision
data processing frameworks (such as Hadoop, Spark and Storm) on
OpenStack by specifying several parameters such as the version,cluster
topology and hardware node details [@www-openStack]. The solution
allows for fast provisioning of data processing clusters on OpenStack
for development and quality assurance and utilisation of unused
computer power from a general purpose OpenStack Iaas
Cloud [@www-Sahara].  Sahara is managed via a REST API with a User
Interface available as part of OpenStack Dashboard.

The rationale behind Sahara is to enable users to easily manage and 
deploy various data processing frameworks with relative ease. While 
users can quickly deploy a cluster within minutes, it is also important 
to note that Sahara enables users to scale existing clusters by
adding/removing nodes on demand. The Sahara product is able to communicate 
with a variety of OpenStack services. Some of the main services that Sahara 
is able to communicate with are Horizon(Dashboards), Keystone(Identification), 
Nova(Computational provisioning), Glance(VM Image storage) and Swift(Object Storage)[@www-fa18-523-88-openstack-sahara].

There are two user cases which can be addressed and summarized via a generic workflow;
cluster provisioning and analytics as a service.



