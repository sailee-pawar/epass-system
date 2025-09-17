document.addEventListener("DOMContentLoaded", function () {
	const chartCanvas = document.getElementById('concessionPieChart');
	if (!chartCanvas) return; // Exit if canvas not present

	const ctx = chartCanvas.getContext('2d');

	// Use data attributes on the canvas to pass counts from Django
	const pending = parseInt(chartCanvas.dataset.pending || 0);
	const rejected = parseInt(chartCanvas.dataset.rejected || 0);
	const approved = parseInt(chartCanvas.dataset.approved || 0);

	const total = pending + rejected + approved;
	console.log("total----"+total);
	if (total === 0) {
		// Option 1: replace chart with a message
		chartCanvas.parentElement.innerHTML = '<p class="text-center mt-3">No concessions taken till now.</p>';

		// Option 2 (optional): render a single blue slice
		const data = {
			labels: ['No Concessions'],
			datasets: [{
				data: [1],
				backgroundColor: ['#007bff'], // Bootstrap blue
				borderColor: '#fff',
				borderWidth: 2
			}]
		};
		new Chart(ctx, { type: 'pie', data: data, options: { responsive: true } });

		return;
	}

	const data = {
		labels: ['Pending', 'Rejected', 'Approved'],
		datasets: [{
			data: [pending, rejected, approved],
			backgroundColor: ['orange', 'red', 'green'],
			borderColor: '#fff',
			borderWidth: 2
		}]
	};

	const config = {
		type: 'pie',
		data: data,
		options: {
			responsive: true,
			plugins: {
				legend: { position: 'bottom' },
				tooltip: {
					callbacks: {
						label: function(context) {
							return context.label + ': ' + context.raw;
						}
					}
				}
			}
		}
	};

	new Chart(ctx, config);
});
