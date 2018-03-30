var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    context: __dirname,
    entry: {
        Room: './rooms/static/js/react/Room', 
	AdminRoom: './rooms/static/js/react/AdminRoom'
    },
    output: {
        path: path.resolve('./rooms/static/bundles/'), 
        filename: '[name]-[hash].js', 
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}), 
    ],
    module: {
        loaders: [
            {
		test: /\.jsx?$/, 
                exclude: /node_modules/, 
                loader: 'babel-loader', 
                query: {
                    presets: ['es2015','react'] 
                }
            },
	    {
                test: /\.scss$/,
		include: path.resolve('./rooms/static/js/react/react-select/'),
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "sass-loader"
                }]
            },
        ]
   },
    resolve: {
        extensions: ['.js', '.jsx', '.scss'] 
    }   
}
