$("document").ready(showCupcakes);

async function showCupcakes() {
	const resp = await axios.get("/api/cupcakes");
	for (let cupcake of resp.data.cupcakes) {
		$("ul").append(
			$("<li>", {
				text: `Flavor: ${cupcake.flavor} Size: ${cupcake.size} Rating: ${cupcake.rating}`,
			})
		);
	}
}

$("form").on("submit", createCupcake);

async function createCupcake(e) {
	e.preventDefault();
	const flavor = $(e.target).find("#flavor").val();
	const rating = $(e.target).find("#rating").val();
	const size = $(e.target).find("#size").val();
	const image = $(e.target).find("#image").val() || null;
	const resp = await axios.post("/api/cupcakes", {
		flavor,
		rating,
		size,
		image,
	});
	let cupcake = resp.data.cupcake;
	$("ul").append(
		$("<li>", {
			text: `Flavor: ${cupcake.flavor} Size: ${cupcake.size} Rating: ${cupcake.rating}`,
		})
	);
	$("form").trigger("reset");
}
