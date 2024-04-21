# 80211bd-heterogeneousPlatooning-EDCA-ReliabilityStudy

This project uses NS3 version 3.36 to simulate network behavior with a focus on enhancing understanding and performance of network protocols under specific conditions. NS3 is a discrete-event network simulator, which is widely used in research and education.

## NS3 Version

This project is developed with [NS3 version 3.36](https://www.nsnam.org/releases/ns-3-36/). NS3 offers detailed and realistic simulations of network protocols, devices, and traffic.

## Prerequisites

Before running this project, ensure you have NS3 installed on your system. This project is specifically tailored for NS3 version 3.36.

## Getting Started

To run this project, follow these steps:

1. **Install NS3 on Your System:**
   - Ensure that NS3 version 3.36 is installed on your machine. Installation guidelines can be found on the [NS3 official website](https://www.nsnam.org/docs/release/3.36/tutorial/html/getting-started.html).

2. **Clone the Project:**
   - Clone this project into the `/scratch` directory of your NS3 installation. This can be done using the following command:
     ```bash
     cd path/to/ns-3.36/scratch
     git clone git@github.com:Sukhija-Aniket/80211bd-heterogeneousPlatooning-EDCA-ReliabilityStudy.gi
     ```

3. **Running the Simulation:**
   - Navigate to your NS3 directory:
     ```bash
     cd path/to/ns-3.36
     ```
   - Run the simulation script located at the root:
     ```bash
     ./mean-delay.sh FILENAME [OPTIONS] 
     ```

   Replace `FILENAME` with the actual name of your simulation script file `test.cc`

## Setting up NS3 for 802.11bd
In order to use 802.11bd, we need to make certain adjustments to the NS3 source code.
The following files need to be changed:
```
src/wave/helper/wave-helper.cc
src/wave/model/wave-net-device.cc 
src/wifi/model/wifi-phy.h
src/wifi/model/frame-exchange-manager.cc
src/wifi/model/wifi-phy.cc
src/wifi/model/wifi-standards.h
src/wifi/model/wifi-phy-operating-channel.cc
src/wifi/model/wifi-remote-station-manager.cc
src/wifi/model/wifi-default-ack-manager.cc 
```

Refer to `codeChanges.pdf` to make these changes and run the project.


## Contributing

Contributions to this project are welcome. Here's how you can contribute:

1. **Fork the Repository:**
   - Fork the project repository to your own GitHub account.

2. **Clone the Fork:**
   - Clone the forked repository to your local machine.

3. **Create a Feature Branch:**
   - Create a new branch for your feature or bug fix.

4. **Commit Changes:**
   - Make your changes in your feature branch and commit them with a clear, descriptive message.

5. **Push to GitHub:**
   - Push your changes to your fork on GitHub.

6. **Submit a Pull Request:**
   - Open a pull request from your feature branch to the main project repository. Describe the changes and improvements introduced.

7. **Review & Merge:**
   - The project maintainers will review your work. If approved, your contributions will be merged into the main project.

## Support

For assistance with issues related to this project, you can:
- Open an issue directly in the GitHub repository for bug reports, feature requests, or other discussions.
- Contact the project maintainers via email for direct support at b20081@students.iitmandi.ac.in

Please include a detailed description of your issue or inquiry for more efficient support.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for contributing to or using this NS3 simulation project!
