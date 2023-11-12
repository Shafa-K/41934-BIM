**Group2_Cost**
The goal of this tool is to support the user calculate the cost of the structural elements in a project.

The way the tool currently works is shown in the IDM-diagram "Current_Use-Case_Group2"

**Model uses**
The primary purpose of this tool/script is to calculate cost estimations for structural elements within a building project. More specifically it finds the size of a structural element and adds a customized property, such as price, to elements in an IFC model. This tool is meant to serve as a vital resource for stakeholders who are involved in the budgeting and planning of a building project. So that can be the project owners and project managers. By providing a detailed breakdown of costs for individual structural elements, it can aid in the decision-making during the project planning and optimize the budget allocations. The tool can also further help with the buildings carbon footprint, because with the detailed overview of the structural elements the engineers can then size down if possible as well as replace some elements with more sustainable materials. That way the tool can be even more enhanced by making it calculate the carbon emissions alongside the cost estimations.

**Process**
Before utilizing the tool, collaboration with the BIM modeler/ the person responsible for generating the IFC file is essential. Accurate geometry and quantities for structural elements must be ensured in the IFC file. After running the script in Blender, the cost estimations are derived based on extracted volumes and areas as well as the material. The information is then communicated to project managers and owners who use it for budgeting, financial planning, and procurement decisions. It's an iterative process, allowing for adjustments based on changing project requirements or cost data.

**Information Exchange**

The tool relies on the Level of Detail within the IFC file. So it is important that the recieved IFC file needs to with the precise geometry and quantities, as well as include the material of the structural elements to be able to get accurate cost estimations. The used IFC model had a sufficient LOD with relevant properties in the file e.g., "Qto_WallBaseQuantities,", "Qto_BeamBaseQuantities" and material assignments. After running the tool the LOD is enhanced with additional customized properties "price" for each element, which makes it possible to calculate a basic price estimation. While the tool currently focuses on basic cost estimations, future advancements may involve incorporating more detailed information, such as a more detailed material layouts, reinforcement in concrete, labor costs, and installment costs etc. The tool is flexible and can adapt to evolving project requirements and industry standards.

With a classification system in place it can also contribute to better categorization and analysis when used with the tool.

**The tool's value(s)**

The tool significantly improves the efficiency of cost estimation processes by automating the addition of prices as customized properties to elements in the IFC model. This way time can be saved by eliminating manual calculations as well provide a detailed cost information to aid decision-makers to make informed choices during project planning and budgeting.

With a better cost overview, project managers have a better chance of identifing costly elements and optimize resources.

The tool also have an environmentally impact by leading to more sustainable choices. Because it enables stakeholders to identify areas where material use can be reduced, contributing to environmentally friendly construction practices. By adopting the tool in future project, it can be an innovative step in the construction industry, promoting the use of technology for sustainable and efficient building practices.

**Further improvements**

As previously mentioned, there is room for further improvement in the tool, particularly in two key areas: the inclusion of carbon emissions calculations and enhancing the Level of Detail (LOD) for more precise price estimations. However, this section will now explore the existing limitations and potential areas for enhancement.

At present, the tool works by assigning a customized property "price" to an object type. This means it can't calculate costs for individual elements; instead, it calculates costs for entire object groups. This limitation is due to both our coding skills and the IfcMaterial setup. In Blender, we couldn't directly attach our a customized property to the material, so we had to do it to the item connected to the material. This requires finding those items and determining a cost for each, which can be time-consuming, affecting the tool's efficiency. The goal is for the tool to simplify project planning, not become a time-consuming process.

Another potential improvement is integrating MOLIO's pricing values (e.g., from Sigma) directly into the tool. Currently, we have to manually add these values separately. Automating this process would enhance the tool's functionality.

The improved functions we wish to implement to the tool is shown in the IDM-diagram "Modified_Use-Case_Group2"
