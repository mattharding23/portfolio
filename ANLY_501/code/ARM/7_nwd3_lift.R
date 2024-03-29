# Create Edge List
edgeList = disp_lift[,c(1:2,5)]
(MyGraph = igraph::simplify(igraph::graph.data.frame(edgeList, directed=TRUE)))

nodeList = data.frame(ID = c(0:(igraph::vcount(MyGraph) - 1)), 
                      nName = igraph::V(MyGraph)$name)
## Create Node List
(nodeList = cbind(nodeList, nodeDegree=igraph::degree(MyGraph, 
                                                      v = igraph::V(MyGraph), mode = "all")))

## Get betweenness
BetweenNess = igraph::betweenness(MyGraph, 
                                  v = igraph::V(MyGraph), 
                                  directed = TRUE) 

(nodeList = cbind(nodeList, nodeBetweenness=BetweenNess))

# Build edges
getNodeID = function(x){
  which(x == igraph::V(MyGraph)$name) - 1  
}

edgeList = plyr::ddply(
  disp_lift, .variables = c("Source", "Target" , "Lift"), 
  function (x) data.frame(SourceID = getNodeID(x$Source), 
                          TargetID = getNodeID(x$Target)))

# Find Dice Sim
DiceSim = igraph::similarity.dice(MyGraph, vids = igraph::V(MyGraph), mode = "all")


# New data frame with Dice similarity between vertices
F1 = function(x) {
  data.frame(diceSim = DiceSim[x$SourceID +1, x$TargetID + 1])
}

# Put Dice Sim column in edgelist
head(edgeList)
edgeList = plyr::ddply(edgeList,
                       .variables=c("Source", "Target", "Lift", 
                                    "SourceID", "TargetID"), 
                       function(x) data.frame(F1(x)))

# Create network 3D display
D3_network_eotb_lift = networkD3::forceNetwork(
  Links = edgeList, # df info about edges
  Nodes = nodeList, # df info about nodes
  Source = "SourceID", # ID of source node 
  Target = "TargetID", # ID of target node
  Value = "Lift", # from the edge list - value/weight relationship amongst nodes
  NodeID = "nName", # from the node list - node description 
  Nodesize = "nodeBetweenness",  # from the node list - node size
  Group = "nodeDegree",  # from the node list - node color
  height = 800, 
  width = 800,  
  fontSize = 20, 
  linkDistance = networkD3::JS("function(d) { return d.value*1000; }"), # Function to determine distance between any two nodes, uses variables already defined in forceNetwork function (not variables from a data frame)
  linkWidth = networkD3::JS("function(d) { return d.value*5; }"),# Function to determine link/edge thickness, uses variables already defined in forceNetwork function (not variables from a data frame)
  opacity = 5, 
  zoom = TRUE, 
  opacityNoHover = 7,
  linkColour = "red"   
) 

# Plot network
D3_network_eotb_lift

# Save Network