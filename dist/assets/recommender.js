
(function () {
  const form = document.getElementById('stack-recommender');
  const output = document.getElementById('recommendation-output');
  if (!form || !output) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    const size = data.get('size');
    const risk = data.get('risk');
    const it = data.get('it');

    const recommendations = [];
    recommendations.push('Password manager with enforced MFA for administrators');
    recommendations.push('Cloud backup with tested restore workflow');

    if (risk === 'ransomware') {
      recommendations.push('Immutable or tamper-resistant backup retention');
      recommendations.push('Documented ransomware recovery runbook');
    }
    if (risk === 'phishing') {
      recommendations.push('Email security / anti-phishing layer');
      recommendations.push('Security awareness training for staff');
    }
    if (risk === 'compliance') {
      recommendations.push('Basic asset inventory and supplier security documentation');
      recommendations.push('Policy templates for access control, backup and incident escalation');
    }
    if (size === 'growing' || it === 'team') {
      recommendations.push('Endpoint protection with central management');
      recommendations.push('Role-based access and admin activity logging');
    }
    if (it === 'none') {
      recommendations.push('Consider a managed service provider for setup and recovery testing');
    }

    output.hidden = false;
    output.innerHTML = '<h2>Recommended first evaluation stack</h2><ol>' + recommendations.map(item => '<li>' + item + '</li>').join('') + '</ol><p><strong>Next:</strong> compare vendors only after these requirements are clear. This is informational guidance, not incident-response or legal advice.</p>';
  });
})();

(function () {
  const form = document.getElementById('rto-rpo-calculator');
  const output = document.getElementById('rto-rpo-output');
  if (!form || !output) return;

  const processLabels = {
    email: 'Email and calendar',
    finance: 'Accounting, billing or payroll',
    client_files: 'Client files or project delivery',
    production: 'Production, booking or revenue system',
    identity: 'Identity, admin or password vault'
  };

  const formatHours = function (hours) {
    if (hours === 0) return 'near-zero data loss';
    if (hours < 1) return Math.round(hours * 60) + ' minutes';
    if (hours === 1) return '1 hour';
    if (hours % 24 === 0) {
      const days = hours / 24;
      return days === 1 ? '1 day' : days + ' days';
    }
    return hours + ' hours';
  };

  const safeNumber = function (formData, key) {
    const value = Number.parseFloat(formData.get(key));
    return Number.isFinite(value) && value >= 0 ? value : 0;
  };

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    const process = processLabels[data.get('process')] || 'Selected process';
    const downtime = Math.max(0.25, safeNumber(data, 'downtime'));
    const dataLoss = safeNumber(data, 'data_loss');
    const people = safeNumber(data, 'people');
    const hourlyCost = safeNumber(data, 'hourly_cost');
    const workaround = data.get('workaround');
    const exposure = downtime * people * hourlyCost;

    let tier = 'Flexible recovery tier';
    let implication = 'A slower, lower-cost backup pattern may be acceptable only if this process is genuinely non-critical and the workaround has been tested.';
    const requirements = [
      'Document the system owner, restore owner and escalation owner.',
      'Run a restore test and keep the date, duration, result and next fix.',
      'Protect backup and administrator accounts with MFA.'
    ];

    if (downtime <= 4 || dataLoss <= 1) {
      tier = 'Critical recovery tier';
      implication = 'The target is tight. Treat this as a managed recovery requirement, not a casual file-backup requirement.';
      requirements.push('Ask vendors for frequent recovery points, immutable or strongly protected retention, tested restore workflows and support response terms.');
    } else if (downtime <= 24 || dataLoss <= 24) {
      tier = 'Standard business-critical tier';
      implication = 'Daily or more frequent automated backup may fit, but only if restore testing proves the target is realistic.';
      requirements.push('Ask vendors for SaaS coverage, clear restore steps, retention policy, admin audit logs and documented recovery testing.');
    } else {
      requirements.push('Write down why slower recovery is acceptable and which workarounds keep the business operating.');
    }

    if (workaround === 'none' && downtime > 24) {
      requirements.push('Because no reliable workaround exists, reconsider whether the RTO can safely exceed 24 hours.');
    }
    if (dataLoss === 0) {
      requirements.push('Near-zero data loss usually requires specialised architecture. Validate feasibility before promising it to clients.');
    }

    const exposureText = exposure > 0
      ? exposure.toLocaleString(undefined, { maximumFractionDigits: 0 }) + ' currency units at the selected RTO'
      : 'not estimated because people or hourly cost is zero';

    output.hidden = false;
    output.innerHTML = '<h2>' + tier + '</h2>' +
      '<p><strong>Process:</strong> ' + process + '</p>' +
      '<ul>' +
      '<li><strong>Suggested RTO:</strong> restore within ' + formatHours(downtime) + ' or faster.</li>' +
      '<li><strong>Suggested RPO:</strong> recover to a point no older than ' + formatHours(dataLoss) + '.</li>' +
      '<li><strong>Approximate staff downtime exposure:</strong> ' + exposureText + '.</li>' +
      '</ul>' +
      '<p><strong>Interpretation:</strong> ' + implication + '</p>' +
      '<h3>Minimum requirements to document</h3><ol>' + requirements.map(item => '<li>' + item + '</li>').join('') + '</ol>' +
      '<p class="microcopy">This is a rough planning estimate. It does not prove that any vendor or internal process can meet the target until a restore test has been completed.</p>';
  });
})();
