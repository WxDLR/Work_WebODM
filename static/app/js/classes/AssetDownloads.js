class AssetDownload{
  constructor(label, asset, icon){
    this.label = label;
    this.asset = asset;
    this.icon = icon;
  }

  downloadUrl(project_id, task_id){
    return `/api/projects/${project_id}/tasks/${task_id}/download/${this.asset}`;
  }

  get separator(){ 
    return false;
  }
}

class AssetDownloadSeparator extends AssetDownload{
  constructor(){
    super("-");
  }

  downloadUrl(){
    return "#";
  }

  get separator(){
    return true;
  }
}

const api = {
  all: function() {
    return [
      new AssetDownload("正摄影像 (GeoTIFF)","orthophoto.tif","fa fa-map-o"),
      new AssetDownload("Orthophoto (PNG)","orthophoto.png","fa fa-picture-o"),
      new AssetDownload("Orthophoto (MBTiles)","orthophoto.mbtiles","fa fa-picture-o"),
      new AssetDownload("Terrain Model (GeoTIFF)","dtm.tif","fa fa-area-chart"),
      new AssetDownload("表面模型 (GeoTIFF)","dsm.tif","fa fa-area-chart"),
      new AssetDownload("点云 (LAS)","georeferenced_model.las","fa fa-cube"),
      new AssetDownload("点云 (LAZ)","georeferenced_model.laz","fa fa-cube"),
      new AssetDownload("点云 (PLY)","georeferenced_model.ply","fa fa-cube"),
      new AssetDownload("点云 (CSV)","georeferenced_model.csv","fa fa-cube"),
      new AssetDownload("已重构模型","textured_model.zip","fa fa-connectdevelop"),
      new AssetDownloadSeparator(),
      new AssetDownload("All Assets","all.zip","fa fa-file-archive-o")
    ];
  },

  excludeSeparators: function(){
    return api.all().filter(asset => !asset.separator);
  },

  // @param assets {String[]} list of assets (example: ['geotiff', 'las']))
  only: function(assets){
    return api.all().filter(asset => assets.indexOf(asset.asset) !== -1);
  }
}

export default api;

