import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

class data_analyzer:
    data = pd.Series({})
    metadata = pd.Series({})
    metadata['n_graph_cluster_pca'] = 0
    report = pd.Series({})
    report['graphs'] = ""


    def __init__(self, name, filepath):
        self.metadata['name'] = name
        df = pd.read_csv(filepath)
        self.data['raw'] = df
        self.data['no_na'] = self.data['raw'].dropna();
        self.metadata['n_removed_na'] = self.data['raw'].shape[0] - self.data['no_na'].shape[0]
        self.data['numerical'] = self.data['no_na'].select_dtypes(exclude=['object'])#.fillna(value=0, axis=1)
        self.data['object'] = self.data['no_na'].select_dtypes(include=['object'])
        self.data['numerical_std'] = pd.DataFrame(StandardScaler().fit_transform(
                self.data['numerical'].values), index=self.data['numerical'].index,
                columns=self.data['numerical'].columns)
        self.metadata['covariance'] = np.cov(self.data['numerical_std'].T)
        self.metadata['eigenvalues'], self.metadata['eigenvectors'] = np.linalg.eig(self.metadata['covariance'])
        self.metadata['eigenvalues_variance_explained'] = [(i/self.metadata['eigenvalues'].sum())*100 for i in sorted(self.metadata['eigenvalues'], reverse=True)]

    def auto(self):
        print(f"Doing basic analysis for {self.metadata['name']}")
        self.base_analysis(95)
        print("Creating graphs")
        self.generate_graphs(0.5)
        print("Creating report")
        self.write()
        print("Auto completed")

    def base_analysis(self, percentage_explained):
        ''' Does a basic analysis on the dataset: PCA'''
        self.metadata['components'] = self.pca_do(self.pre_pca(percentage_explained))
        self.metadata['max_correlations'] = self.best_correlation()

    def generate_graphs(self, threshold):
        self.graph_variance_explained()
        self.graph_covariance_heatmap(threshold)
        self.graph_pca_pairs()

    def pre_pca(self, percentage_explained):
        '''Returns number of components needed to explain percentage of variance explained'''
        total = 0
        n = 1

        for value in self.metadata['eigenvalues_variance_explained']:
            total = total + value
            #print(f"{value} --- {total}.....{n}") # Ok for debug

            if total > percentage_explained:
                return n

            n = n + 1

    def pca_do(self, components):
        '''Does a PCA'''
        pca = PCA(n_components=components)
        self.data['PCA'] = pca.fit_transform(self.data['numerical_std'])

        return components

    def graph_variance_explained(self):
        '''Creates a graph over variance explains as a function of principle components'''
        n_columns = self.data['numerical'].shape[1]
        plt.figure(figsize=(10, 5))
        plt.bar(range(n_columns), self.metadata['eigenvalues_variance_explained'], alpha=0.3333, align='center', label='individual explained variance', color = 'g')
        plt.axhline(y=95, linewidth=1, color='r', linestyle='dashed', label="95%")
        plt.axhline(y=90, linewidth=1, color='r', linestyle='dashed', label="90%")
        plt.step(range(n_columns), np.cumsum(self.metadata['eigenvalues_variance_explained']), where='mid',label='cumulative explained variance')
        plt.ylabel('Explained variance ratio')
        plt.xlabel('Principal components')
        plt.legend(loc='best')
        plt.title('Individual and cumulative variance explained')
        plt.savefig(f"{self.metadata['name']}_variance_explained.png")
        self.report['graphs'] = self.report['graphs'] + f'''<h2>Variance explained 90% - 95%</h2><center><img 
src="{self.metadata['name']}_variance_explained.png"></img></center>'''

    def graph_pca_pairs(self):
        '''Plots data from PCA dimensional perspectives'''
        sns_plot = sns.pairplot(pd.DataFrame(self.data['PCA']))
        sns_plot.savefig(f"{self.metadata['name']}_pca_pairs.png")

        self.report['graphs'] = self.report['graphs'] + f'''<h2>Pairwise plot of PCA using {self.metadata['components']} principle components</h2><center><img 
src="{self.metadata['name']}_pca_pairs.png"></img></center>'''


    def graph_covariance_heatmap(self, threshold):
        '''Generates a covariance matrix visualized by a heatmap'''
        self.metadata['numerical_correlation'] = self.data['numerical'].corr()
        plt.subplots() #figsize=(15, 12)
        plt.title('Pearson Correlation of Movie Features')

        # Mask to remove diagonal and upper half
        mask = np.zeros_like(self.metadata['numerical_correlation'], dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        ax = sns.heatmap(self.metadata['numerical_correlation'],vmax=1,square=True,annot=True,mask=mask);


        for cell in ax.texts:
            if (abs(float(cell.get_text())) > threshold):
                ax.add_patch(Rectangle((int(cell.get_position()[0]-0.5),
                                        int(cell.get_position()[1]-0.5)), 1, 1,
                                        fill=False, edgecolor='blue', lw=2))

        ax.get_figure().savefig(f"{self.metadata['name']}_covariance_heatmap.png")
        self.report['graphs'] = self.report['graphs'] + f'''<h2>Covariance heatmap with threshold {0.5}</h2><center><img 
src="{self.metadata['name']}_covariance_heatmap.png"></img></center>'''

    def cluster_pca(self, clusters):
        self.metadata['clusters'] = clusters
        kmeans = KMeans(n_clusters=clusters)
        self.data['numerical'].is_copy = False
        self.data['numerical']['X_cluster'] = kmeans.fit_predict(self.data['PCA'])
        self.data[f'clustered_{clusters}'] = {}


        for i in range(clusters):
            self.data[f'clustered_{clusters}'][i] = (self.data['numerical'][self.data['numerical']['X_cluster'] == i])

    def graph_cluster_pca(self, components):
        print(f"running {self.metadata['n_graph_cluster_pca']}")
        graphname = f"{self.metadata['name']}_cluster_pca{self.metadata['n_graph_cluster_pca']}.png"
        df = pd.DataFrame(self.data['PCA'])
        df = df[list(range(components))]
        df['X_cluster'] = self.data['numerical']['X_cluster']
        sns_plot = sns.pairplot(df, hue='X_cluster', palette='Dark2', diag_kind='kde',size=1.85)
        sns_plot.savefig(graphname)

        self.report['graphs'] = self.report['graphs'] + f'''<h2> K-means clustering with {self.metadata['clusters']} clusters</h2><center><img 
src="{graphname}"></img></center>'''

        self.metadata['n_graph_cluster_pca'] += 1

    def best_correlation(self):
        df = self.data['numerical'].corr()
        np.fill_diagonal(df.values, 0)
        pairs = df.idxmax()
        pred = []
        a = []
        b = []
        for i in range(pairs.shape[0]):
            pred.append(df.get_value(pairs.index[i], pairs[i]))
            a.append(pairs.index[i])
            b.append(pairs[i])
    
        pred = pd.DataFrame(pred)
        pred['a'] = a
        pred['b'] = b
            
        return pred

    def graph_categorical(self):
        '''Overview of categorical data'''
        pass

    def object_to_onehot(self):
        self.data['object'][self.data['object'].isnull().any(axis=1)]
        cols = self.data['object'].columns.values.tolist()
        self.data['object_onehot'] = pd.concat([pd.get_dummies(self.data['object'], columns=cols, prefix=cols), self.data['object'].drop(cols, 1)], 1)

    def object_group_median(self, groups):
        df = pd.DataFrame([])
        for column in self.data['numerical'].columns.values:    
            df[column] = self.data['no_na'].groupby(groups)[column].apply(np.median)
        
        self.metadata['grouped_median'] = df

    def status(self):
        print(self.data.keys())

    def write(self):
        '''Generates full html report for dataset'''
        with open(f"{self.metadata['name']}_report.html", 'w') as file:
            file.write(f'''
<html>
    <head>
        <title>{self.metadata['name']}</title>
    </head>
        <body>
        <center><h1>{self.metadata['name']}</h1></center>
        This is an auto-generated dataset report!
        <h2>Dataset summary</h2>
        Generated data keys: {list(self.data.keys())}<br>
        Generated metadata keys: {list(self.metadata.keys())}<br>
        {self.data['numerical'].describe().to_html()}
        {self.report['graphs']}
        </body>
</html>
                       ''')

if __name__ == "__main__":
    datasets = {}
    datasets['sal'] = data_analyzer("college_salaries", "../datasets/college-salaries/salaries-by-college-type.csv_clean");
    datasets['sal'].base_analysis(90)
    datasets['sal'].object_group_median('School Type')
#    datasets['sal'].auto() 

    #hr = data_analyzer("hr_data", "../datasets/human-resources-analytics/HR_comma_sep.csv");
    #hr.base_analysis(percentage_explained=90)
    #hr.auto()
    pass

#%% Class for data_cleaner
class data_cleaner:
    df = pd.DataFrame([])
    filepath = ""
    
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.filepath = filepath
        pass
    
    def fix_currency_usd(self):
        df = pd.read_csv("../datasets/college-salaries/salaries-by-college-type.csv")
        df = df.dropna()

        for i in range(2, df.shape[1]):
            df.iloc[:,i] = df.iloc[:,i].replace("""[\$,)]""",'', regex=True).replace( '[(]','-',   regex=True ).astype(float)
    
        df.to_csv(f"{self.filepath}_clean")
        
dc = data_cleaner("../datasets/college-salaries/salaries-by-college-type.csv")
dc.fix_currency_usd()


#%% Investigation


def pca_investigate(data, investigations):
    for i in range(len(data)):
        print(f"n[{i}]: {data[i].shape[0]}")
        for column in investigations:
            print(f"{column} mean: {data[i][column].mean()}")

#pca_investigate(pubg.data['clustered_2'],["solo_Wins", "solo_RoundsPlayed", "solo_WinRatio"])
#sns.regplot(x=pubg.data['PCA'][0], y=pubg.data['PCA'][2], marker="+")
#sns.pairplot()
#pubg.data['numerical'].shape
#pubg.graph_covariance_heatmap(0.5)

#%%

    # Human resources dataset
    hr = data_analyzer("hr_data", "../../datasets/human-resources-analytics/HR_comma_sep.csv");
    hr.auto()
    hr.base_analysis(percentage_explained=90)
    hr.graph_covariance_heatmap(0.5)
    hr.graph_variance_explained()
    hr.graph_pca_pairs()
    hr.generate_graphs(threshold=0.5)
    hr.cluster_pca(clusters=2)
    hr.graph_cluster_pca(components=3)
    hr.cluster_pca(clusters=3)
    hr.graph_cluster_pca(components=3)
    hr.cluster_pca(clusters=4)
    hr.graph_cluster_pca(components=3)
    hr.write()

    # IMDB movie dataset
    movie = data_analyzer("imdb", "../../datasets/movie_metadata.csv");
    #movie.auto()
    #movie.base_analysis(percentage_explained=90)
    #movie.generate_graphs(threshold=0.5)
    #movie.cluster_pca(clusters=2)
    #movie.graph_cluster_pca(components=3)
    #movie.write()

        # IMDB movie dataset
    #house = data_analyzer("house", "../../datasets/housesalesprediction/kc_house_data.csv");
    #house.auto()
    #house.base_analysis(percentage_explained=90)
    #house.generate_graphs(threshold=0.5)
    #house.cluster_pca(clusters=2)
    #house.graph_cluster_pca(components=3)
    #house.write()
