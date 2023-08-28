.PHONY: all clean

all: gpus.txt

clean:
	rm -f *.yaml *.csv *.txt

nodes.yaml:
	kubectl get nodes -o yaml > $@

node-gpus.csv: nodes.yaml
	echo 'node,gpu' > $@
	cat nodes.yaml | yq -r '.items[].metadata | "\(.name),\(.labels."nvidia.com/gpu.product")"' >> $@

# use tail to skip first 2 lines (gpu and null)
gpus.txt: node-gpus.csv
	xsv select gpu node-gpus.csv | sort | uniq | tail -n +3 > $@
