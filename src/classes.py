import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class BioprocessMonitor:

    def __init__(self, filepath, ph_lims, temperature_lims):
        """ Utility class used to monitor bioprocesses by
                         generating dashboards and summaries.
                         Parameters
                         ----------
                         filepath : str
                             Input CSV dataset path.
                         ph_lims : tuple[float, float]
                             Lower and upper acceptable pH limits.
                         temperature_lims : tuple[float, float]
                             Lower and upper acceptable temperature limits."""
        self.filepath = filepath
        self.ph_min = ph_lims[0]
        self.ph_max = ph_lims[1]
        self.temperature_min = temperature_lims[0]
        self.temperature_max = temperature_lims[1]

        #input dataset_fermentation.csv
        self.data = pd.read_csv(filepath)

    def extract_batch(self, batch_id):
        """Extracts data corresponding to a single batch.
                            Parameters
                            ----------
                            batch_id : int
                                Batch identifier.
                            Returns
                            -------
                            pandas.DataFrame
                                DataFrame containing only rows associated with
                                the requested batch."""
        return self.data[self.data.batch_id == batch_id]

    def optimal_ph_mask(self, df_batch):
        """
         Determines whether each pH measurement falls within
           the acceptable operating range.

               Parameters
               ----------
               df_batch : pandas.DataFrame
                   Batch-specific DataFrame.
               Returns
               -------
               array-like of bool
                   A mask whereby True indicates that the measurement
                   is within the acceptable operating range.
               """
        ph_ok = (df_batch ["pH"] >= self.ph_min) & (df_batch ["pH"] <= self.ph_max)
        return ph_ok

    def optimal_temperature_mask(self, df_batch):
        """
         Determines whether each temperature measurement falls
         within the acceptable operating range.
               Parameters
               ----------
               df_batch : pandas.DataFrame
                   Batch-specific DataFrame.

               Returns
               -------
               array-like of bool
                   A mask whereby True indicates that the measurement
                   is within the acceptable operating range.
               """
        temperature_ok = (df_batch["temperature_C"] >= self.temperature_min) & (df_batch["temperature_C"] <= self.temperature_max)
        return temperature_ok


    def get_n_batches(self):
        """
        Determines the number of unique batches present
        in the dataset.
        Returns
        -------
        int
            Total number of distinct batch identifiers.
        """
        return self.data["batch_id"].nunique()

    def export_dashboard(self, batch_id, filepath):
        df_batch = self.extract_batch(batch_id)

        fig, ax = plt.subplots(2,2,figsize=(10, 8), dpi=200)
        # Top left: ax[0,0]
        # Top right: ax[0,1]
        # Bottom left: ax[1,0]
        # Bottom right: ax[1,1]

       # Top left plot
        ax[0,0].scatter(df_batch["time_h"], df_batch["C_glucose_g_L^-1"],
                   color="tab:blue", marker="o", label="Glucose", s = 16, alpha = 0.7, edgecolors = "black", linewidth = 0.5 )

        ax[0,0].scatter(df_batch["time_h"], df_batch["C_biomass_g_L^-1"],
                   color="tab:purple", marker="s", label="Biomass", s=16, alpha=0.7, edgecolors="black", linewidth=0.5)

        ax[0,0].scatter(df_batch["time_h"], df_batch["C_product_g_L^-1"],
                   color="tab:orange", marker="^", label="Product Concentration", s=16, alpha=0.7, edgecolors="black", linewidth=0.5)

        ax[0,0].set_xlabel("Time (h)")
        ax[0,0].set_ylabel("Concentration (g/L)")
        ax[0,0].legend()

        #Top Right plot
        temperature_ok = self.optimal_temperature_mask(df_batch)

        ax[0,1].scatter(df_batch.loc[temperature_ok, "time_h"], df_batch.loc[temperature_ok, "temperature_C"],
                   color="tab:green", marker="o", label="Temperature OK", s=16, alpha=0.7, edgecolors="black", linewidth=0.5)

        ax[0,1].scatter(df_batch.loc[~temperature_ok, "time_h"], df_batch.loc[~temperature_ok, "temperature_C"],
                   color="tab:red", marker="X", label="Temperature Out of Range", s=16, alpha=0.7, edgecolors="black", linewidth=0.5)

        ax[0,1].set_xlabel("Time (h)")
        ax[0,1].set_ylabel("Temperature (C)")
        ax[0,1].legend()

        #bottom left plot
        ph_ok = self.optimal_ph_mask(df_batch)

        ax[1,0].scatter(df_batch.loc[ph_ok, "time_h"], df_batch.loc[ph_ok, "pH"],
                   color="tab:green", marker="o", label="pH OK", s=16, alpha=0.7, edgecolors="black",
                   linewidth=0.5)

        ax[1,0].scatter(df_batch.loc[~ph_ok, "time_h"], df_batch.loc[~ph_ok, "pH"],
                   color="tab:red", marker="X", label="pH Out of Range", s=16, alpha=0.7, edgecolors="black",
                   linewidth=0.5)

        ax[1,0].set_xlabel("Time (h)")
        ax[1,0].set_ylabel("pH")
        ax[1,0].legend()

        #bottom right plot
        ax[1,1].scatter(df_batch.loc[:,"time_h"], df_batch.loc[:,"DO_percent"],
                   color="tab:pink", marker="o", label="Dissolved Oxygen", s=16, alpha=0.7, edgecolors="black",
                   linewidth=0.5)

        ax[1,1].set_xlabel("Time (h)")
        ax[1,1].set_ylabel("Dissolved Oxygen (%)")

        # tick spacing of 6h
        ax[0,0].xaxis.set_major_locator(MultipleLocator(6))
        ax[0,1].xaxis.set_major_locator(MultipleLocator(6))
        ax[1,0].xaxis.set_major_locator(MultipleLocator(6))
        ax[1,1].xaxis.set_major_locator(MultipleLocator(6))

        #saving and closing files
        fig.savefig(filepath)
        plt.close(fig)

        """
        Creates and saves a dashboard figure for a single batch.

        Parameters
        ----------
        batch_id : int
            Batch identifier.
        filepath : str
            Output PNG image path.

        Dashboard Requirements
        ----------------------
        Create a 2 × 2 figure containing:

        Top-Left
            Glucose, biomass, and product concentrations versus time.
            - A different color and marker should be used for each substance.
        Top-Right
            Temperature versus time.
            - Measurements within the acceptable temperature range
              should be displayed as green circles.
            - Measurements outside the acceptable temperature range
              should be displayed as red X markers.

        Bottom-Left
            pH versus time.
            - Measurements within the acceptable pH range
              should be displayed as green circles.
            - Measurements outside the acceptable pH range
              should be displayed as red X markers.
        Bottom-Right
            Dissolved oxygen versus time.

        Additional Requirements
        -----------------------
        - Use scatter plots.
        - Add x-axis and y-axis labels.
        - Add legends where appropriate.
        - Apply consistent formatting across all subplots unless
          indicated otherwise.
        - Apply a tick spacing of 6 h on the x-axis for all subplots.
        - Save the figure to the provided filepath.
        - Close the figure after saving.
        """

    def export_summary(self, filepath):
        summary = []
        for batch_id in range(1,self.get_n_batches() + 1):
            df_batch = self.extract_batch(batch_id)

            # for pH
            ph_mask = self.optimal_ph_mask(df_batch)
            ph_percent = round(ph_mask.mean() * 100, 2)

            # for temperature
            temperature_mask = self.optimal_temperature_mask(df_batch)
            temperature_percent = round(temperature_mask.mean() * 100, 2)

            final_product = df_batch["C_product_g_L^-1"].iloc[-1]

            summary.append({
                "batch_id": batch_id,"ph_optimal_percent": ph_percent, "temperature_optimal_percent": temperature_percent,
                "C_product_g_L^-1_final": final_product})

        summary_df = pd.DataFrame(summary)
        summary_df.to_csv(filepath, index=False)
        """
        Generates a batch summary table and exports it to a CSV file.

        Parameters
        ----------
        filepath : str
            Output CSV table path.

        Summary Table Columns
        ---------------------
        batch_id
            Batch identifier.

        ph_optimal_percent
            Percentage of measurements in a batch within the
            acceptable pH range, rounded to 2 decimal places.

        temperature_optimal_percent
            Percentage of measurements in a batch within the
            acceptable temperature range, rounded to 2 decimal places.

        C_product_g_L^-1_final
            Final product concentration for the batch.
        """