(defun gps-line ()
  "Print the current buffer line number and total number of lines (that end in a newline)."
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos)))
    (if (= start 1)
	(message "Line %d / %d" n (count-lines (point-min) (point-max)))
      (save-excursion
	(save-restriction
          (widen)
          (let ((current-line (+ n (line-number-at-pos start) -1))
		(total-lines (count-lines (point-min) (point-max))))
            (message "Current line: %d / Total lines: %d" current-line total-lines)))))))

