<script lang="ts">
  import Button, { Icon, Label } from "@smui/button";
  import "@smui/button/bare.css";

  async function saveImage() {
    const canvas = document.getElementById(
      "simulationCanvas"
    ) as HTMLCanvasElement;
    const writable = await showSaveFilePicker({
      excludeAcceptAllOption: true,
      types: [
        {
          description: "Image",
          accept: {
            "image/png": [".png"],
          },
        },
      ],
    }).then((handle) => handle.createWritable());
    canvas.toBlob((blob) => {
      writable.write(blob);
      writable.close();
    }, "image/png");
  }
</script>

<div class="buttons">
  <Button variant="outlined" on:click={saveImage}>
    <Icon class="material-icons">download</Icon>
    <Label>Save</Label>
  </Button>
</div>

<style>
  .buttons {
    margin: 1em 2.4em;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    justify-self: end;
  }
</style>
