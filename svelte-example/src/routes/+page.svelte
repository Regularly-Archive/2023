<script>
    let count = 0;
    let position = { x: 0, y: 0 };
    let person = "秦元培";
    $: alert =  `用户正在输入：${person}`;
    function incrementCount() {
        count += 1;
    }
    function handleMouseMove(e) {
        position.x = e.clientX;
        position.y = e.clientY;
    }
</script>

<h1>Welcome to SvelteKit</h1>
<p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
</p>

<button on:click={incrementCount}>
    点击 {count} 次
</button>

<div class="container" on:mousemove={handleMouseMove}>
    当前鼠标位置是: ({position.x}, {position.y})
</div>

<hr />

<input bind:value={person} />
<p>{alert}</p>

<style>
    .container {
        background: #ccc;
        height: 200px;
        width: 100%;
        margin-top: 20px;
    }
</style>
