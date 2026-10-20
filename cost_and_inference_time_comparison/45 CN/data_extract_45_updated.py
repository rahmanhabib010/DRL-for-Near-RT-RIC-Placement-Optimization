import ast
import json
import numpy as np

# Open the JSON file

def process_topology(file_path):

    with open(file_path, 'r') as file:
        # Load the data from the file
        data = json.load(file)

    # Now, 'data' contains the parsed JSON data as a Python dictionary
    #print(data.keys()) #dict_keys(['links', 'CNs', 'E2 Nodes'])


    df1=data["CNs"]

    # Required keys
    required_keys = ['ID', 'Type', 'CPU', 'Fixed_cost', 'ET', 'SD', 'DB', 'XP']

    # Extract dictionaries containing all required keys
    filtered_df1 = [d for d in df1 if all(key in d for key in required_keys)]


    # Lists to store IDs based on the layer
    cloud_layer = []
    regional_layer = []
    edge_layer = []

    # Process CNS (Cloud Nodes)
    for node in df1:
        if node["Type"] == "Cloud Node":
            cloud_layer.append(node["ID"])

    # Process E2 Nodes (Regional and Edge Nodes)
    for node in filtered_df1:
        if node["Type"] == "Regional Node":
            regional_layer.append(node["ID"])
        elif node["Type"] == "Edge Node":
            edge_layer.append(node["ID"])


    # # Convert the arrays to strings
    # cloud_layer_str = list(map(str, cloud_layer))
    # regional_layer_str = list(map(str, regional_layer))
    # edge_layer_str = list(map(str, edge_layer))

#    Number of nodes
    N = len(cloud_layer)+len(regional_layer)+len(edge_layer)

    # Initialize latency matrix with default value (30 for missing links)
    latency_matrix = np.full((N, N), 30)

    # Fill in latency values from topology data
    for entry in data["links"]:
        node_pair = ast.literal_eval(entry["link"])  # Safely convert "(a, b)" to tuple
        latency = entry["delay"]

        # Assign latency to both (a, b) and (b, a) since it's bidirectional
        latency_matrix[node_pair[0], node_pair[1]] = latency
        latency_matrix[node_pair[1], node_pair[0]] = latency  # Ensure symmetry

    # # Output the IDs for each layer
    # # print("Cloud Layer IDs:", cloud_layer_str)
    # # print("Regional Layer IDs:", regional_layer_str)
    # # print("Edge Layer IDs:", edge_layer_str)

    # # Function to extract delays between specific layers
    # delays=data["links"]
    # #print(len(delays))
    # def extract_delays(links, source_ids, target_ids):
    #     delays = []
    #     for link_data in links:
    #         # Extract the link information (e.g., (0, 11), (1, 12), etc.)
    #         link = link_data["link"].strip("()").split(", ")
    #         source = int(link[0])
    #         target = int(link[1])
            
    #         # Check if the link is between source and target layers
    #         if (source in source_ids and target in target_ids) or (source in target_ids and target in source_ids):
    #             delays.append({"link": link_data["link"], "delay": link_data["delay"]})
        
    #     return delays

    # # Extract delays between Cloud and Edge layer
    # cloud_edge_delays = extract_delays(delays, cloud_layer, edge_layer)

    # # Extract delays between Regional and Edge layer
    # regional_edge_delays = extract_delays(delays, regional_layer, edge_layer)

    # # Extract delays between Edge layer
    # edge_delays = extract_delays(delays, edge_layer, edge_layer)


    # # # Output results
    # # print("Cloud-E2 Layer Delays:", cloud_edge_delays)
    # # print("Regional-E2 Layer Delays:", regional_edge_delays)
    # #print("Edge-E2 Layer Delays:", edge_delays)


    # #Function to combine loop links
    # def combine_bidirectional_links(links):
    #     combined_links = {}
        
    #     for link_data in links:
    #         # Extract the link and sort it (e.g., (0, 11) and (11, 0) both become (0, 11))
    #         link = tuple(sorted(link_data["link"].strip("()").split(", ")))
    #         delay = link_data["delay"]
            
    #         # If the link (sorted) already exists, add the delay to the existing entry
    #         if link in combined_links:
    #             combined_links[link] += delay
    #         else:
    #             combined_links[link] = delay
        
    #     # Return the combined links as a list of dicts
    #     return [{"link": f"({link[0]}, {link[1]})", "delay": delay} for link, delay in combined_links.items()]

    # # Combine Cloud-Edge and Regional-Edge delays
    # combined_cloud_edge = combine_bidirectional_links(cloud_edge_delays)
    # combined_regional_edge = combine_bidirectional_links(regional_edge_delays)

    # # # Output the results
    # # print("Combined Cloud-Edge Layer Delays:", combined_cloud_edge)
    # # print("Combined Regional-Edge Layer Delays:", combined_regional_edge)

    # #Function to combine Edge loop links

    # def combine_edge_links(links):
    #     combined_links = {}
        
    #     for link_data in links:
    #         link = tuple(link_data["link"].strip("()").split(", "))
    #         delay = link_data["delay"]
            
    #         # If the link (sorted) already exists, add the delay to the existing entry
    #         if link in combined_links:
    #             combined_links[link] += delay
    #         else:
    #             combined_links[link] = delay
        
    #     # Return the combined links as a list of dicts
    #     return [{"link": f"({link[0]}, {link[1]})", "delay": delay} for link, delay in combined_links.items()]
    
    # combined_edge=[]

    # for i in edge_layer:
    #     arr=[]
    #     for entry in edge_delays:
    #         values = list(map(int, entry['link'].strip('()').split(', ')))
    #         if i== values[0]:
    #             # print(entry)
    #             arr.append(entry)

    #         elif i==values[1]:
    #             link_values = tuple(reversed(eval(entry['link'])))
    #             entry['link'] = str(link_values)
    #             # print(entry)
    #             arr.append(entry)
    #         else:
    #             pass
    #     data=combine_edge_links(arr)
    #     combined_edge.append(sorted(data, key=lambda x: int(x['link'].split(', ')[1].strip(')'))))


    # # Extracting delay values
    # cloud_edge_delays = np.array([d['delay'] for d in combined_cloud_edge])  # (53,)
    # regional_edge_delays = np.array([d['delay'] for d in combined_regional_edge])# (530,)
    # print(regional_edge_delays.shape)
    # edge_e2_delays = np.array([[entry['delay'] for entry in sublist] for sublist in combined_edge]) #(53,53)

    # # print(cloud_edge_delays.shape)
    # # print(regional_edge_delays.shape)

    # reshaped_regional = regional_edge_delays.reshape(20, 107)

    # # Step 2: Reshape cloud_edge_delays to (53, 1)
    # reshaped_cloud = cloud_edge_delays.reshape(1, 107)

    # # Step 3: Concatenate the two arrays
    # combined_array = np.concatenate((reshaped_cloud, reshaped_regional, edge_e2_delays), axis=0)

    # # Print the resulting combined array and its shape
    # # print(combined_array)
    # # print("Shape of the combined array:", combined_array.shape)

    return cloud_layer, regional_layer, edge_layer, latency_matrix*2
