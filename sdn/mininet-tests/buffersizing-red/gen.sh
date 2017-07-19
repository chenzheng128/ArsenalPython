
rootdir=red-p0.02-Jul17-23-13/
python plot-results.py --dir $rootdir --out red-p0.02.png

# 使用内嵌4项数据生成图表 for flows_per_host in 10 25 50 100; 
python plot-results.py --dir $rootdir --out red-embed.png -e
