
download:
	./downloadbsp.sh satellites jup310

deploy: latest_leapseconds.tls spp_nom_20180812_20250831_v037_R04.bsp
	gcloud app deploy

show_logs:
	gcloud app logs tail -s default

delete_old_versions:
	gcloud app versions delete --quiet `gcloud app versions list --filter="version.createTime<-P1D" --format="value(id)"`
