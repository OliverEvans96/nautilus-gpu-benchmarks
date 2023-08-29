.PHONY: all clean

all: gpus.txt 4090-node.yaml a100-node.yaml

clean:
	rm -f *.yaml *.csv *.txt

nodes.yaml:
	kubectl get nodes -o yaml > $@

node-gpus.csv: nodes.yaml
	echo 'node,gpu' > $@
	cat nodes.yaml | yq -r '.items[].metadata | "\(.name),\(.labels."nvidia.com/gpu.product")"' >> $@

# use tail to skip first 2 lines (gpu and null)
gpus.txt: node-gpus.csv
	xsv select gpu node-gpus.csv | sort | uniq -c | tail -n +3 > $@

4090-node.yaml: nodes.yaml
	cat nodes.yaml | yq -y '.items[] | select(.metadata.name == "k8s-4090-01.calit2.optiputer.net")' > $@

a100-node.yaml: nodes.yaml
	cat nodes.yaml | yq -y '.items[] | select(.metadata.name == "k8s-a100-01.calit2.optiputer.net")' > $@
