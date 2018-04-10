# Thesis
### Improving Network Protocol Uptime During Upgrades Through Component Containerization
Research work for my M.S. in CS thesis, a.k.a. "really bad but functional code"

The idea is to come up with an architecture for a dissagregated NOS which is built on top of containerized services. The theory is this approach allows us to upgrade individual components of the system without taking the entire NOS down. The paper explores this idea from the context of protocol downtime. Specifically, our measured variable is the downtime of a simple BGP implementation during a rolling four host upgrade of the BGP service.