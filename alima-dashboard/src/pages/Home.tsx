import { useState, useEffect } from "react";
import Plot from "react-plotly.js";

function Home() {
  const [fftX, setFftX] = useState([]);
  const [fftY, setFftY] = useState([]);
  const [fftZ, setFftZ] = useState([]);
  const [timeSecs, setTimeSecs] = useState([]);

  const [posFreqX, setPosFreqX] = useState([]);
  const [posFreqY, setPosFreqY] = useState([]);
  const [posFreqZ, setPosFreqZ] = useState([]);

  const [freqValsX, setFreqValsX] = useState([]);
  const [freqValsY, setFreqValsY] = useState([]);
  const [freqValsZ, setFreqValsZ] = useState([]);

  const getData = () => {
    //fetch GET to http://localhost:5000/graph_values which returns JSON
    fetch("http://localhost:5000/graph_values")
      .then((response) => response.json())
      .then((data) => {
        setFftX(data.fft_x);
        setFftY(data.fft_y);
        setFftZ(data.fft_z);
        setTimeSecs(data.time_secs);

        setPosFreqX(data.pos_freq_x);
        setPosFreqY(data.pos_freq_y);
        setPosFreqZ(data.pos_freq_z);

        setFreqValsX(data.freq_vals_x);
        setFreqValsY(data.freq_vals_y);
        setFreqValsZ(data.freq_vals_z);
      });
  };

  useEffect(() => {
    getData(); // get data on page load

    const timer = setInterval(() => {
      // reload data every 5 seconds
      getData();
    }, 5000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="header-2">
      <nav className="bg-white py-1 md:py-2">
        <div className="container px-4 mx-auto md:flex md:items-center">
          <div className="flex justify-between items-center">
            <img
              src="https://i.postimg.cc/8knx6QBc/pzD6DkJ.png"
              alt="intelimek"
            />
          </div>
          {/*   <div class="hidden md:flex flex-col md:flex-row md:ml-auto mt-3 md:mt-0" id="navbar-collapse">
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-white rounded bg-indigo-600">Home</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-gray-600 rounded hover:bg-gray-200 hover:text-gray-700 transition-colors duration-300">About</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-gray-600 rounded hover:bg-gray-200 hover:text-gray-700 transition-colors duration-300">Features</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-gray-600 rounded hover:bg-gray-200 hover:text-gray-700 transition-colors duration-300">Pricing</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-gray-600 rounded hover:bg-gray-200 hover:text-gray-700 transition-colors duration-300">Contact</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-indigo-600 text-center border border-transparent rounded hover:bg-indigo-100 hover:text-indigo-700 transition-colors duration-300">Login</a>
                <a href="#" class="p-2 lg:px-4 md:mx-2 text-indigo-600 text-center border border-solid border-indigo-600 rounded hover:bg-indigo-600 hover:text-white transition-colors duration-300 mt-1 md:mt-0 md:ml-1">Signup</a>
              </div>  */}
        </div>
      </nav>
      <div className="bg-indigo-100 py-3">
        <div className="container px-4 mx-auto">
          <div className="flex flex-wrap justify-center text-center mb-4 mt-6">
            <div className="w-full px-4">
              <h2 className="text-4xl font-semibold text-slate-900">
                Sensor Values
              </h2>
              <p className="text-lg leading-relaxed m-4 text-slate-600">
                This page displays the sensor values from the accelerometer. The
                values are updated every 5 seconds.
              </p>
            </div>
          </div>

          <div className="grid gap-3 px-4 py-4 max grid-cols-2">
            <Plot
              className="shadow-md"
              data={[
                {
                  x: timeSecs,
                  y: fftX,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "X-Axis Acceleration vs Time",
                xaxis: { title: "Time (Secs)" },
                yaxis: { title: "A-X (m/s^2)" },
              }}
            />

            <Plot
              className="shadow-md"
              data={[
                {
                  x: posFreqX,
                  y: freqValsX,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "X-Axis FFT Plot",
                xaxis: { title: "Frequency (Hz)" },
                yaxis: { title: "Amplitude" },
              }}
            />

            <Plot
              className="shadow-md"
              data={[
                {
                  x: timeSecs,
                  y: fftY,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "Y-Axis Acceleration vs Time",
                xaxis: { title: "Time (Secs)" },
                yaxis: { title: "A-Y (m/s^2)" },
              }}
            />

            <Plot
              className="shadow-md"
              data={[
                {
                  x: posFreqY,
                  y: freqValsY,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "Y-Axis FFT Plot",
                xaxis: { title: "Frequency (Hz)" },
                yaxis: { title: "Amplitude" },
              }}
            />

            <Plot
              className="shadow-md"
              data={[
                {
                  x: timeSecs,
                  y: fftZ,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "Z-Axis Acceleration vs Time",
                xaxis: { title: "Time (Secs)" },
                yaxis: { title: "A-Z (m/s^2)" },
              }}
            />

            <Plot
              className="shadow-md"
              data={[
                {
                  x: posFreqZ,
                  y: freqValsZ,
                  type: "scatter",
                },
              ]}
              layout={{
                title: "Z-Axis FFT Plot",
                xaxis: { title: "Frequency (Hz)" },
                yaxis: { title: "Amplitude" },
              }}
            />
          </div>

          {/* <img
                src="http://127.0.0.1:5000/get_plots.png"
                alt="get_plots"
                className="d-block max-w-full rounded shadow-md"
              /> */}

          {/* <div className="p-64 bg-green-500"></div> */}
          {/* <div class="md:flex md:flex-wrap md:-mx-4 mt-6 md:mt-12">*/}
          {/*                <div class="md:w-1/3 md:px-4 xl:px-6 mt-8 md:mt-0 text-center">*/}
          {/*                    <span class="w-20 border-t-2 border-solid border-indigo-200 inline-block mb-3"></span>*/}
          {/*                    <h5 class="text-xl font-medium uppercase mb-4">Fresh Design</h5>*/}
          {/*                    <p class="text-gray-600">FWR blocks bring in an air of fresh design with their creative layouts and*/}
          {/*                        blocks, which are easily customizable</p>*/}
          {/*                </div>*/}
          {/*                <div class="md:w-1/3 md:px-4 xl:px-6 mt-8 md:mt-0 text-center">*/}
          {/*                    <span class="w-20 border-t-2 border-solid border-indigo-200 inline-block mb-3"></span>*/}
          {/*                    <h5 class="text-xl font-medium uppercase mb-4">Clean Code</h5>*/}
          {/*                    <p class="text-gray-600">FWR blocks are the cleanest pieces of HTML blocks, which are built with*/}
          {/*                        utmost care to quality and usability.</p>*/}
          {/*                </div>*/}
          {/*                <div class="md:w-1/3 md:px-4 xl:px-6 mt-8 md:mt-0 text-center">*/}
          {/*                    <span class="w-20 border-t-2 border-solid border-indigo-200 inline-block mb-3"></span>*/}
          {/*                    <h5 class="text-xl font-medium uppercase mb-4">Perfect Tool</h5>*/}
          {/*                    <p class="text-gray-600">FWR blocks is a perfect tool for designers, developers and agencies looking*/}
          {/*                        to create stunning websites in no time.</p>*/}
          {/*                </div>*/}
          {/*            </div> */}
        </div>
      </div>
    </div>
  );
}

export default Home;
