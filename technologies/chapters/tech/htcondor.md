## HTCondor :o:


|          |                             |
| -------- | --------------------------- |
| title    | HTCondor                    | 
| status   | 10                          |
| section  | Cluster Resource Management |
| keywords | Cluster Resource Management |


HTCondor was originally developed thru years of research at the University 
of Wisconsin-Madison's Department of Computer Sciences. A division within 
the department focuses on High Throughput Computing and was successful in 
deploying a production system internally for the department over 15 years 
ago. It has since grown to be used by organizations spanning industries, 
governemtn departments and unversities across the world, with installations 
leveraging a couple workstations all the way up to thousands of 
workstations [@www-fa18-523-88-htcondor].
    
HTCondor is a specialized workload management system for
compute-intensive jobs.  HTCondor provides various features like (a) job
queuing mechanism, (b) scheduling policy, (c) resource monitoring,
(d) priority scheme and (e) resource management just as other
full-featured batch systems.

> ``Users submit their serial or parallel jobs to HTCondor,HTCondor
> places them into a queue, chooses when and where to run the jobs
> based upon a policy, carefully monitors their progress, and
> ultimately informs the user upon completion''.

HTCondor can be used to manage a cluster of dedicated compute nodes. 
HTCondor uses unique mechanisms to harness wasted CPU power from idle 
desktopworkstations.

> ``The ClassAd mechanism in HTCondor provides an extremely flexible
> and expressive framework for matching resource requests (jobs) with
> resource offers (machines).  Jobs can easily state both job
> requirements and job preferences. HTCondor incorporates many of the
> emerging Grid and Cloud-based computing methodologies and
> protocols'' [@htcondor].

Because HTCondor does not rely on a shared file system between machines, 
if one does not exist, HTCondor will transfer any data files needed for 
the job on behalf of the user. Alternatively, HTCondor may also be able 
to redirect all I/O requests submitted by the job back to the submitting 
machine. This allows HTCondor to harnesss all of the computational power
within an organization's domain to perform process intensive jobs [@www-fa18-523-88-htcondor].
